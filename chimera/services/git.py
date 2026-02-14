import asyncio
from pathlib import Path

from langchain.tools import tool

from chimera.services.utils import live_stream
from chimera.settings import GIT_PATH, GIT_WORKTREE_PATH


@tool("git-worktree-create-tool", description="Create a git worktree from the target directory")
async def git_worktree_create(target_path: Path, branch_name: str) -> Path:
    worktree_path = GIT_WORKTREE_PATH / branch_name
    call = [GIT_PATH, "worktree", "add", "-b", branch_name, worktree_path]
    process = await asyncio.create_subprocess_exec(
        *call, cwd=target_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    if not process.stdout or not process.stderr:
        process.kill()
        raise AttributeError("stdout/stderr is None")

    await asyncio.gather(live_stream(process.stdout), live_stream(process.stderr))
    return worktree_path


@tool("git-worktree-remove-tool", description="Remove a git worktree from the target directory")
async def git_worktree_remove(target_path: Path, worktree_path: Path):
    call = [GIT_PATH, "worktree", "remove", worktree_path]
    process = await asyncio.create_subprocess_exec(
        *call, cwd=target_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    if not process.stdout or not process.stderr:
        process.kill()
        raise AttributeError("stdout/stderr is None")

    await asyncio.gather(live_stream(process.stdout), live_stream(process.stderr))


@tool("git-commit-tool", description="Make a git commit with a message in the target directory")
async def git_commit(target_path: Path, message: str):
    process = await asyncio.create_subprocess_exec(
        GIT_PATH,
        "commit",
        "-m",
        message,
        cwd=target_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if not process.stdout or not process.stderr:
        process.kill()
        raise AttributeError("stdout/stderr is None")

    await asyncio.gather(live_stream(process.stdout), live_stream(process.stderr))


@tool("git-push-tool", description="Make a git push in the target directory")
async def git_push(target_path: Path):
    process = await asyncio.create_subprocess_exec(
        GIT_PATH, "push", cwd=target_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    if not process.stdout or not process.stderr:
        process.kill()
        raise AttributeError("stdout/stderr is None")

    await asyncio.gather(live_stream(process.stdout), live_stream(process.stderr))
