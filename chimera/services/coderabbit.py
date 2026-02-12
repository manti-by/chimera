import asyncio
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models.context import Context
from chimera.settings import CODERABBIT_PATH


@tool("review-agent", description="Coderabbit agent used to review changed code more in depth")
async def review_agent(task: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return await run_coderabbit_agent(project_path, task)


async def run_coderabbit_agent(project_path: Path, task: str) -> str:
    call = [CODERABBIT_PATH, "review", "--prompt-only", "--no-color", "--type", "uncommitted", task]
    proc = await asyncio.create_subprocess_exec(
        *call, cwd=project_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    return stdout.decode()
