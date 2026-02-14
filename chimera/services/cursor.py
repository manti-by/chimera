from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models import Context
from chimera.services.prompt import get_prompt
from chimera.services.subprocess import run_command
from chimera.settings import CURSOR_PATH


@tool("review-agent", description="Coderabbit agent used to review changed code more in depth")
async def review_agent(runtime: ToolRuntime[Context]) -> str:
    if not runtime.context.worktree_path:
        raise ValueError("Worktree path is not set")

    worktree_path = runtime.context.worktree_path
    task = await get_prompt(name="review")
    return await run_cursor_agent(target_path=worktree_path, task=task)


async def run_cursor_agent(target_path: Path, task: str) -> str:
    command = [CURSOR_PATH, "--plan", "--print", task, "--force"]
    return await run_command(command=command, target_path=target_path)
