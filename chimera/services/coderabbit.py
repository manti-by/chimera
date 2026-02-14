import asyncio
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models import Context
from chimera.services.utils import live_stream
from chimera.settings import CODERABBIT_PATH


@tool("review-agent", description="Coderabbit agent used to review changed code more in depth")
async def review_agent(runtime: ToolRuntime[Context]):
    if not runtime.context.worktree_path:
        raise ValueError("Worktree path is not set")

    worktree_path = runtime.context.worktree_path
    return await run_coderabbit_agent(target_path=worktree_path)


async def run_coderabbit_agent(target_path: Path) -> str:
    call = [CODERABBIT_PATH, "review", "--prompt-only", "--no-color", "--type", "uncommitted"]
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
