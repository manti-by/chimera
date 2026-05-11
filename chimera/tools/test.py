from pathlib import Path

from langchain.tools import tool

from chimera.services.subprocess import run_command
from chimera.settings import UV


@tool("pytest-tool", description="Run pytest tests with the --lf (last-failed) flag in the target directory")
async def pytest_tool(target_path: Path) -> tuple[int, str, str]:
    return await run_command(
        command=[str(UV["path"]), "run", "--active", "pytest", "--lf", "--quiet", "--color=no"], target_path=target_path
    )
