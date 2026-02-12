import asyncio
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models.context import Context
from chimera.settings import OPENCODE_PATH


@tool("plan-agent", description="Opencode agent used to plan a feature implementation")
async def plan_agent(task: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return await run_opencode_agent(project_path, task, agent="plan")


@tool("build-agent", description="Opencode agent used to build a feature")
async def build_agent(task: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return await run_opencode_agent(project_path, task, agent="build")


async def run_opencode_agent(project_path: Path, task: str, agent: str = "plan") -> str:
    task = task + "\nFollow the instructions in the AGENTS.md for Git and Linear workflows."
    call = [OPENCODE_PATH, "--agent", agent, "--prompt", task, "--model", "opencode/minimax-m2.1-free", "--quiet"]
    proc = await asyncio.create_subprocess_exec(
        *call, cwd=project_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()
