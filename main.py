import argparse
import asyncio

from deepagents import CompiledSubAgent, create_deep_agent
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mistralai import ChatMistralAI

from chimera.models.context import Context
from chimera.services.coderabbit import review_agent
from chimera.services.filesystem import get_project_root
from chimera.services.linear import get_linear_mcp_config
from chimera.services.opencode import build_agent, plan_agent


parser = argparse.ArgumentParser(prog="chimera", description="Run AI workflow.", add_help=True)
parser.add_argument("-p", "--project-name", help="Project name to run workflow on", type=str)

chat_model = ChatMistralAI(temperature=0.7, max_tokens=1024)


def opencode_plan_subagent() -> CompiledSubAgent:
    custom_graph = create_agent(model=chat_model, tools=[plan_agent], system_prompt="You are a great feature planner")
    return CompiledSubAgent(name="plan-agent", description="Used to plan feature implementation", runnable=custom_graph)


def opencode_build_subagent() -> CompiledSubAgent:
    custom_graph = create_agent(model=chat_model, tools=[build_agent], system_prompt="You are a great feature builder")
    return CompiledSubAgent(
        name="build-agent", description="Used to build feature implementation", runnable=custom_graph
    )


def coderabbit_review_subagent() -> CompiledSubAgent:
    custom_graph = create_agent(model=chat_model, tools=[review_agent], system_prompt="You are a great code reviewer")
    return CompiledSubAgent(
        name="review-agent", description="Used to review changed code more in depth", runnable=custom_graph
    )


async def main(project_name: str):
    project_path = get_project_root(project_name)

    linear_config = get_linear_mcp_config()
    mcp_clients = MultiServerMCPClient({"linear": linear_config})  # ty: ignore[invalid-argument-type]
    tools = await mcp_clients.get_tools()

    system_prompt = (
        "You are a helpful personal assistant. "
        "You can retrieve tasks from Linear, plan and build them using OpenCode and review them using Coderabbit. "
        "Break down user requests into appropriate tool calls and coordinate the results. "
        "When a request involves multiple actions, use multiple tools in sequence."
    )
    supervisor_agent = create_deep_agent(
        chat_model,
        name="supervisor",
        subagents=[opencode_plan_subagent(), opencode_build_subagent(), coderabbit_review_subagent()],
        interrupt_on={"plan-agent": True, "build-agent": True, "review-agent": False},
        tools=tools,
        system_prompt=system_prompt,
        context_schema=Context,
    )

    project_path = get_project_root(project_name)
    context = Context(project_name=project_name, project_path=project_path)

    query = (
        f"1. Retrieve the latest Linear task for {project_name} project from TODO column. "
        "2. Create an implementation plan for the task using OpenCode. "
        "3. Wait for user input to proceed. If it is necessary return to a previous step. "
        "4. Build the feature using OpenCode. "
        "5. Check feature using Coderabbit. If there are some suggestions, pass them to the previous step and repeat the previous steps."
    )
    payload = {"messages": [{"role": "user", "content": query}]}
    async for step in supervisor_agent.astream(payload, context=context):  # ty: ignore[invalid-argument-type]
        print(step)


if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(project_name=args.project_name))
