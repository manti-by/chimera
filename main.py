import argparse
import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, START, StateGraph

from chimera.services.linear import get_linear_mcp_config
from chimera.services.prompt import get_prompt
from chimera.services.terminal import print_heading, print_message
from chimera.tools import get_available_tools


logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog="chimera", description="Run AI workflow.", add_help=True)
parser.add_argument("-p", "--project-name", help="Project name to run workflow on", type=str)


@dataclass
class WorkflowState:
    messages: list[BaseMessage] = field(default_factory=list)
    llm_calls: int = 0
    project_name: str = ""
    linear_task_id: str | None = None
    branch_name: str | None = None
    worktree_path: Path | None = None
    implementation_plan: str | None = None
    build_attempts: int = 0
    review_attempts: int = 0
    needs_rebuild: bool = False
    needs_relint: bool = False
    lint_errors: str | None = None
    test_errors: str | None = None
    pr_url: str | None = None


async def llm_call(state: WorkflowState, chat_model, tools_by_name: dict) -> dict[str, Any]:
    system_content = await get_prompt(name="system")
    messages: list[BaseMessage] = [SystemMessage(content=system_content)]
    for msg in state.messages:
        messages.append(msg)

    response = chat_model.invoke(messages)
    return {"messages": [response], "llm_calls": state.llm_calls + 1}


async def tool_node(state: WorkflowState, tools_by_name: dict) -> dict[str, Any]:
    last_message = state.messages[-1]
    if not hasattr(last_message, "tool_calls"):
        return {"messages": []}

    tool_calls = getattr(last_message, "tool_calls", None)
    if not tool_calls:
        return {"messages": []}

    results: list[BaseMessage] = []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        args = tool_call["args"]
        try:
            if asyncio.iscoroutinefunction(tool.func):
                observation = await tool.func(**args)
            else:
                observation = tool.func(**args)
        except Exception as e:  # noqa: BLE001
            observation = f"Error: {e!s}"
        results.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))

    return {"messages": results}


def should_continue(state: WorkflowState) -> str:
    last_message = state.messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool_node"
    return END


async def main(project_name: str):
    await print_heading()
    print_message(f"Starting workflow for project: {project_name}", style="heading")

    chat_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, max_tokens=4096, max_retries=2)

    linear_config = get_linear_mcp_config()
    mcp_clients = MultiServerMCPClient(cast(dict, {"linear": linear_config}))
    remote_tools = await mcp_clients.get_tools()

    tools = [*await get_available_tools(), *remote_tools]
    tools_by_name = {tool.name: tool for tool in tools}

    initial_state = WorkflowState(
        messages=[HumanMessage(content=f"Start the feature development workflow for project: {project_name}")],
        project_name=project_name or "",
    )

    agent_builder = StateGraph(WorkflowState)

    agent_builder.add_node("llm_call", lambda state: asyncio.run(llm_call(state, chat_model, tools_by_name)))
    agent_builder.add_node("tool_node", lambda state: asyncio.run(tool_node(state, tools_by_name)))

    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    agent_builder.add_edge("tool_node", "llm_call")

    agent = agent_builder.compile()

    await agent.ainvoke(initial_state)  # type: ignore[arg-type]


if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(project_name=args.project_name))
