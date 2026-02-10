import subprocess  # nosec
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models.context import Context
from chimera.settings import CODERABBIT_PATH


@tool("review-agent", description="Used to review changed code more in depth")
async def review_agent(query: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return run_coderabbit_agent(project_path, query)


def run_coderabbit_agent(project_path: Path, query: str) -> str:
    result = subprocess.run(
        [CODERABBIT_PATH, "review", "--prompt-only", "--no-color", "--type", "uncommitted", query],  # nosec
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    return result.stdout
