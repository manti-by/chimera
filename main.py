import argparse
import asyncio
import shutil

from deepagents import create_deep_agent
from langchain.messages import AIMessageChunk, ToolMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, Interrupt

from chimera.models.context import Context
from chimera.services.coderabbit import review_agent
from chimera.services.filesystem import get_project_root
from chimera.services.linear import get_linear_task
from chimera.services.opencode import build_agent, plan_agent
from chimera.services.prompt import get_prompt


parser = argparse.ArgumentParser(prog="chimera", description="Run AI workflow.", add_help=True)
parser.add_argument("-p", "--project-name", help="Project name to run workflow on", type=str)

chat_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, max_tokens=512, max_retries=2)


async def print_message(message: str):
    COLOR, ENDC = "\x1b[2m", "\033[0m"
    size = shutil.get_terminal_size((80, 20))

    print(f"\n{message}\n")
    print(COLOR + "-" * size.columns + ENDC)


async def handle_interrupt(interrupt_data: Interrupt) -> list[dict]:
    action_requests = interrupt_data.value.get("action_requests", [])
    review_configs = interrupt_data.value.get("review_configs", [])
    config_map = {cfg["action_name"]: cfg for cfg in review_configs}

    print("\n" + "=" * 50)
    print("🤖 ACTION REQUIRES APPROVAL")
    print("=" * 50)

    decisions = []
    for action in action_requests:
        action_name = action.get("name", "unknown")
        action_args = action.get("args", {})
        review_config = config_map.get(action_name, {})
        allowed_decisions = review_config.get("allowed_decisions", ["approve", "edit", "reject"])

        print(f"\nTool: {action_name}")
        print(f"Arguments: {action_args}")
        print(f"Allowed decisions: {', '.join(allowed_decisions)}")

        decision = await get_user_decision(action_name, allowed_decisions)
        decisions.append(decision)

    print("=" * 50 + "\n")
    return decisions


async def get_user_decision(action_name: str, allowed_decisions: list[str]) -> dict:
    print(f"\nHow would you like to proceed with '{action_name}'?")
    for i, decision in enumerate(allowed_decisions, 1):
        print(f"  [{i}] {decision}")

    while True:
        try:
            choice = input(f"Enter your choice (1-{len(allowed_decisions)}): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(allowed_decisions):
                decision_type = allowed_decisions[idx]
                break
        except (ValueError, IndexError):
            pass
        print("Invalid choice. Please try again.")

    if decision_type == "edit":
        print(f"\nOriginal args: {await get_current_args(action_name)}")
        edited_args = await get_edited_args(action_name)
        return {"type": "edit", "edited_action": {"name": action_name, "args": edited_args}}

    return {"type": decision_type}


async def get_current_args(action_name: str) -> str:
    return "(see above)"


async def get_edited_args(action_name: str) -> dict:
    print("\nEnter edited arguments (leave empty to keep original, comma-separated key=value pairs):")
    user_input = input("  ").strip()
    if not user_input:
        return {}

    args = {}
    for pair in user_input.split(","):
        if "=" in pair:
            key, value = pair.split("=", 1)
            args[key.strip()] = value.strip()
    return args


async def run_with_hitl(agent, payload: dict, config: dict, context: Context):
    while True:
        async for step_type, data in agent.astream(
            payload,
            config=config,
            context=context,
            stream_mode=["messages", "updates"],
        ):
            if step_type == "messages":
                message, metadata = data
                if isinstance(message, ToolMessage):
                    if message.name in ["linear-task", "plan-agent", "build-agent", "review-agent"]:
                        await print_message(f"{message.name}:\n\n{message.content}")
                        continue

                if isinstance(message, AIMessageChunk):
                    await print_message(f"Call node:\n{metadata}")
                    continue

                await print_message(f"Unknown message:\n{message}\n{metadata}")
                continue

            elif step_type == "updates":
                if "__interrupt__" in data:
                    decisions = await handle_interrupt(interrupt_data=data["__interrupt__"][0])
                    await agent.ainvoke(
                        Command(resume={"decisions": decisions}),
                        config=config,
                        context=context,
                    )
                    continue

                await print_message(f"Update: {data.keys()}")
                continue

            await print_message(f"Unknown step {step_type}: {data}")


async def main(project_name: str):
    system_prompt = await get_prompt(name="system")
    supervisor_agent = create_deep_agent(
        chat_model,
        name="supervisor",
        tools=[get_linear_task, plan_agent, build_agent, review_agent],
        interrupt_on={
            "linear-task": False,
            "plan-agent": False,
            "build-agent": True,
            "review-agent": False,
        },
        system_prompt=system_prompt,
        context_schema=Context,
        checkpointer=MemorySaver(),
    )

    query = await get_prompt(name="workflow", project_name=project_name)
    payload = {"messages": [{"role": "user", "content": query}]}

    config = {"configurable": {"thread_id": "conversation_1"}}

    project_path = get_project_root(project_name)
    context = Context(project_name=project_name, project_path=project_path)

    await run_with_hitl(agent=supervisor_agent, payload=payload, config=config, context=context)


if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(project_name=args.project_name))
