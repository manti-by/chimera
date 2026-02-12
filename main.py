import argparse
import asyncio

from deepagents import create_deep_agent
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from chimera.models.context import Context
from chimera.services.coderabbit import review_agent
from chimera.services.filesystem import get_project_root
from chimera.services.linear import get_linear_task
from chimera.services.opencode import build_agent, plan_agent
from chimera.services.prompt import get_prompt


parser = argparse.ArgumentParser(prog="chimera", description="Run AI workflow.", add_help=True)
parser.add_argument("-p", "--project-name", help="Project name to run workflow on", type=str)

chat_model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3, max_tokens=512, max_retries=2)


async def main(project_name: str):
    project_path = get_project_root(project_name)

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

    config: RunnableConfig = {"configurable": {"thread_id": "conversation_1"}}
    context = Context(project_name=project_name, project_path=project_path)

    async for message in supervisor_agent.astream(payload, config=config, context=context):  # ty: ignore
        print(message)


if __name__ == "__main__":
    args = parser.parse_args()
    asyncio.run(main(project_name=args.project_name))
