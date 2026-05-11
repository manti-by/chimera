from pathlib import Path

from langchain.tools import tool

from chimera.services.subprocess import run_command
from chimera.settings import GITHUB


@tool("github-create-pull-request-tool", description="Create a Pull Request for the current branch")
async def create_pull_request(target_path: Path, branch_name: str, title: str, base: str = "master") -> bool:
    command = [
        str(GITHUB["path"]),
        "pr",
        "create",
        "--base",
        base,
        "--head",
        branch_name,
        "--title",
        title,
        "--body",
        "",
    ]
    exit_code, _, _ = await run_command(command=command, target_path=target_path)
    return not exit_code
