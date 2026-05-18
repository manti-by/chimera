import asyncio
from typing import Any, cast

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, START, StateGraph

from chimera.library.models import WorkflowState
from chimera.services.linear import get_linear_mcp_config
from chimera.services.prompt import get_prompt
from chimera.services.terminal import print_message
from chimera.settings import GROQ, MAX_BUILD_ATTEMPTS, MAX_REVIEW_ATTEMPTS
from chimera.tools import get_available_tools
from chimera.tools.opencode import PLAN_HAS_QUESTIONS, PLAN_HEADER_STRING, PLAN_IS_READY_STRING


async def llm_call(state: WorkflowState, chat_model, tools_by_name: dict) -> dict[str, Any]:
    print_message(f"[llm_call/async] Starting. llm_calls={state.llm_calls}, messages={len(state.messages)}")

    system_content = await get_prompt(
        name="system",
        project_name=state.project_name,
        worktree_path=str(state.worktree_path)
        if state.worktree_path
        else f"/home/manti/.chimera/worktrees/opencode/feature/{state.project_name}",
        project_path=f"/home/manti/www/{state.project_name}",
    )
    messages: list[BaseMessage] = [SystemMessage(content=system_content)]
    messages.extend(state.messages)

    if len(messages) > 20:
        messages = messages[:1] + messages[-19:]

    print_message(f"[llm_call/async] Invoking chat model with {len(messages)} messages...")
    response = await chat_model.ainvoke(messages)

    new_messages = list(state.messages)
    new_messages.append(response)

    print_message(
        f"[llm_call/async] Got response. type={type(response).__name__}, tool_calls={bool(getattr(response, 'tool_calls', None))}"
    )
    return {"messages": new_messages, "llm_calls": state.llm_calls + 1}


async def tool_node(state: WorkflowState, tools_by_name: dict) -> dict[str, Any]:
    last_message = state.messages[-1]
    if not hasattr(last_message, "tool_calls"):
        print_message("[tool_node/async] No tool_calls attribute")
        return {"messages": []}

    tool_calls = getattr(last_message, "tool_calls", None)
    if not tool_calls:
        print_message("[tool_node/async] tool_calls is empty or None")
        return {"messages": []}

    print_message(f"[tool_node/async] Processing {len(tool_calls)} tool calls")
    results: list[BaseMessage] = []
    updates: dict[str, Any] = {}
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        print_message(f"[tool_node/async] Executing tool: {tool_name}")
        tool = tools_by_name.get(tool_name)
        if not tool:
            print_message(f"[tool_node/async] Tool '{tool_name}' not found in tools_by_name")
            observation = f"Error: Tool '{tool_name}' not found"
        else:
            args = tool_call["args"]
            print_message(f"[tool_node/async] Tool args: {args}")
            try:
                if hasattr(tool, "coroutine") and tool.coroutine:
                    observation = await tool.coroutine(**args)
                elif asyncio.iscoroutinefunction(tool.func):
                    observation = await tool.func(**args)
                elif tool.func:
                    observation = tool.func(**args)
                else:
                    observation = await tool.invoke(args)
                print_message(
                    f"[tool_node/async] Tool result type: {type(observation).__name__}, length: {len(str(observation))}"
                )
            except Exception as e:  # noqa: BLE001
                observation = f"Error: {e!s}"
                print_message(f"[tool_node/async] Tool error: {observation}")

        if tool_name == "build-agent-tool":
            updates["build_attempts"] = state.build_attempts + 1
            print_message(f"[tool_node/async] build_attempts: {state.build_attempts} -> {updates['build_attempts']}")

        if tool_name == "review-agents-tool":
            updates["review_attempts"] = state.review_attempts + 1
            print_message(f"[tool_node/async] review_attempts: {state.review_attempts} -> {updates['review_attempts']}")
            # Check if review found issues
            review_text = str(observation).lower()
            if any(word in review_text for word in ["issue", "error", "fix", "problem", "fail"]):
                updates["needs_rebuild"] = True
                print_message("[tool_node/async] Review found issues, setting needs_rebuild=True")
            else:
                print_message("[tool_node/async] Review passed")

        if tool_name == "plan-agent-tool":
            plan_text = str(observation)
            if PLAN_HAS_QUESTIONS in plan_text:
                print_message("[tool_node/async] Plan has questions, waiting for user input")
            elif PLAN_HEADER_STRING in plan_text:
                header_idx = plan_text.index(PLAN_HEADER_STRING)
                plan_content = plan_text[header_idx + len(PLAN_HEADER_STRING) :].strip()
                if PLAN_IS_READY_STRING in plan_content:
                    plan_content = plan_content.replace(PLAN_IS_READY_STRING, "").strip()
                updates["implementation_plan"] = plan_content
                updates["needs_rebuild"] = False
                print_message(f"[tool_node/async] Extracted implementation plan, length: {len(plan_content)}")

        if tool_name == "git-worktree-create-tool":
            if not str(observation).startswith("Error:"):
                # Store the worktree path from successful creation
                try:
                    from pathlib import Path

                    updates["worktree_path"] = Path(str(observation))
                    print_message(f"[tool_node/async] Stored worktree_path: {updates['worktree_path']}")
                except (ValueError, TypeError):
                    print_message("[tool_node/async] Could not parse worktree_path")

        if tool_name in ["ruff-lint-tool", "pytest-tool"]:
            if not str(observation).startswith("Error:"):
                updates["needs_relint"] = False
                print_message(f"[tool_node/async] {tool_name} passed, setting needs_relint=False")
            else:
                updates["needs_rebuild"] = True
                print_message(f"[tool_node/async] {tool_name} failed, setting needs_rebuild=True")

        # Track completed steps
        completed = list(state.completed_steps)
        if tool_name not in completed:
            completed.append(tool_name)
            updates["completed_steps"] = completed

        results.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))

    new_messages = list(state.messages)
    new_messages.extend(results)

    return {"messages": new_messages, **updates}


def _sync_llm_call(state: WorkflowState, chat_model, tools_by_name: dict) -> dict[str, Any]:
    try:
        result = asyncio.run(llm_call(state, chat_model, tools_by_name))
        print_message(
            f"[llm_call] Completed. returning: messages={len(result.get('messages', []))}, llm_calls={result.get('llm_calls', 0)}"
        )
        return result
    except Exception as e:  # noqa: BLE001
        print_message(f"[llm_call] ERROR: {type(e).__name__}: {e}")
        raise


def _sync_tool_node(state: WorkflowState, tools_by_name: dict) -> dict[str, Any]:
    print_message(f"[tool_node] Starting. messages: {len(state.messages)}")
    try:
        result = asyncio.run(tool_node(state, tools_by_name))
        print_message(f"[tool_node] Completed. returning: messages={len(result.get('messages', []))}")
        return result
    except Exception as e:  # noqa: BLE001
        print_message(f"[tool_node] ERROR: {type(e).__name__}: {e}")
        raise


def should_continue(state: WorkflowState) -> str:
    last_message = state.messages[-1]
    content = str(last_message.content) if hasattr(last_message, "content") else ""

    has_tool_calls = hasattr(last_message, "tool_calls") and last_message.tool_calls
    if has_tool_calls:
        tc = cast(list, last_message.tool_calls)
        print_message(f"[should_continue] tool_calls → tool_node ({len(tc)} calls)")
        return "tool_node"

    if PLAN_HAS_QUESTIONS in content:
        print_message("[should_continue] Plan has questions → END")
        return END

    if state.build_attempts >= MAX_BUILD_ATTEMPTS:
        print_message("[should_continue] Max build attempts reached → END")
        return END

    if state.review_attempts >= MAX_REVIEW_ATTEMPTS:
        print_message("[should_continue] Max review attempts reached → END")
        return END

    # If we need to rebuild (either initial or after review/lint failure)
    if state.needs_rebuild:
        print_message(f"[should_continue] needs_rebuild={state.needs_rebuild} → llm_call")
        return "llm_call"

    # If we need to run lint/test
    if state.needs_relint:
        print_message(f"[should_continue] needs_relint={state.needs_relint} → llm_call")
        return "llm_call"

    # If plan is ready but not yet built
    if state.implementation_plan and state.build_attempts == 0:
        print_message("[should_continue] Plan ready, no builds yet → llm_call")
        return "llm_call"

    # Check if workflow is complete
    required_final_steps = [
        "git-commit-tool",
        "git-push-tool",
        "github-create-pull-request-tool",
        "git-worktree-remove-tool",
    ]
    if all(step in state.completed_steps for step in required_final_steps):
        print_message("[should_continue] Workflow complete → END")
        return END

    # If we have a plan and have done some building, continue to let LLM decide next steps
    if state.implementation_plan and state.build_attempts > 0:
        print_message("[should_continue] Build in progress → llm_call")
        return "llm_call"

    print_message("[should_continue] No tool calls, no special conditions → END")
    return END


async def run(project_name: str) -> None:
    print_message(f"Starting workflow for project: {project_name}", style="heading")

    if not project_name:
        print_message("Please provide the project name", style="error")

    chat_model = ChatGroq(model=GROQ["model"], temperature=0.0, max_tokens=8192, max_retries=2)

    print_message("└ done", style="info")

    print_message("Setup tools", style="result")

    try:
        linear_config = get_linear_mcp_config()
        mcp_clients = MultiServerMCPClient(cast(dict, {"linear": linear_config}))
        remote_tools = await mcp_clients.get_tools()
        print_message(f"MCP tools loaded: {len(remote_tools)}", style="info")
    except Exception as e:  # noqa: BLE001
        print_message(f"Warning: MCP setup failed: {e}. Using local tools only.", style="warning")
        remote_tools = []

    tools = await get_available_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    chat_model_with_tools = chat_model.bind_tools(tools)

    print_message(f"Local tools: {len(tools)}", style="info")

    print_message("└ done", style="info")

    print_message("Set initial workflow state", style="result")

    prompt = f"Start the feature development workflow for project: {project_name}"
    initial_state = WorkflowState(messages=[HumanMessage(content=prompt)], project_name=project_name)

    print_message("└ done", style="info")

    print_message("Building state graph", style="result")

    agent_builder = StateGraph(WorkflowState)

    agent_builder.add_node("llm_call", lambda state: _sync_llm_call(state, chat_model_with_tools, tools_by_name))
    agent_builder.add_node("tool_node", lambda state: _sync_tool_node(state, tools_by_name))

    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", "llm_call", END])
    agent_builder.add_edge("tool_node", "llm_call")

    agent = agent_builder.compile()

    print_message("└ done", style="info")

    print_message("Invoke the Agent", style="result")

    try:
        await agent.ainvoke(initial_state)  # type: ignore[arg-type]
    except Exception as e:  # noqa: BLE001
        print_message(f"[run] Agent invocation failed: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()
    else:
        print_message("[run] Agent invocation completed successfully")
