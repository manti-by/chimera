import asyncio
import shlex
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models import Context
from chimera.services.utils import live_stream
from chimera.settings import OPENCODE_MODEL, OPENCODE_PATH


@tool("plan-agent", description="Opencode agent used to plan a feature implementation")
async def plan_agent(task: str, runtime: ToolRuntime[Context], repeat: bool = False):
    if not runtime.context.worktree_path:
        raise ValueError("Worktree path is not set")

    worktree_path = runtime.context.worktree_path
    return await run_opencode_agent(target_path=worktree_path, task=task, repeat=repeat, agent="plan")


@tool("build-agent", description="Opencode agent used to build a feature")
async def build_agent(task: str, runtime: ToolRuntime[Context], repeat: bool = False):
    if not runtime.context.worktree_path:
        raise ValueError("Worktree path is not set")

    worktree_path = runtime.context.worktree_path
    return await run_opencode_agent(target_path=worktree_path, task=task, repeat=repeat, agent="build")


async def run_opencode_agent(target_path: Path, task: str, repeat: bool = False, agent: str = "plan") -> str:
    call = [OPENCODE_PATH, "run", "--model", OPENCODE_MODEL, "--agent", agent]
    if repeat:
        call.append("--continue")
    call.append(shlex.quote(task))

    process = await asyncio.create_subprocess_exec(
        *call, cwd=target_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    if not process.stdout or not process.stderr:
        process.kill()
        raise AttributeError("stdout/stderr is None")

    result = []
    await asyncio.gather(live_stream(process.stdout, result=result), live_stream(process.stderr))
    await process.wait()
    return "".join(result)
