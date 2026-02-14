import shlex
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models import Context
from chimera.services.subprocess import run_command
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
    command = [OPENCODE_PATH, "run", "--model", OPENCODE_MODEL, "--agent", agent]
    if repeat:
        command.append("--continue")
    command.append(shlex.quote(task))
    return await run_command(command=command, target_path=target_path)
