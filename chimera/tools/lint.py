from pathlib import Path

from langchain.tools import tool

from chimera.services.subprocess import run_command
from chimera.settings import UV


@tool("ruff-format-tool", description="Run RUFF formatting tool")
async def run_ruff_format(target_path: Path) -> tuple[int, str, str]:
    return await run_command(
        command=[str(UV["path"]), "run", "--active", "ruff", "format", "--silent"], target_path=target_path
    )


@tool("ruff-lint-tool", description="Run RUFF linter")
async def run_ruff_checks(target_path: Path, session_id: str | None = None) -> tuple[int, str, str]:
    return await run_command(
        command=[str(UV["path"]), "run", "--active", "ruff", "check", "--quiet"], target_path=target_path
    )
