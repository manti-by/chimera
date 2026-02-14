from pathlib import Path

from langchain.tools import tool

from chimera.services.subprocess import run_command
from chimera.services.tui import print_message
from chimera.settings import GIT_PATH, GIT_WORKTREE_PATH


@tool("git-worktree-create-tool", description="Create a git worktree from the target directory")
async def git_worktree_create(target_path: Path, branch_name: str) -> Path:
    worktree_path = GIT_WORKTREE_PATH / branch_name
    command = [GIT_PATH, "worktree", "add", "-b", branch_name, worktree_path]
    await run_command(command=command, target_path=target_path)
    return worktree_path


@tool("git-worktree-remove-tool", description="Remove a git worktree from the target directory")
async def git_worktree_remove(target_path: Path, worktree_path: Path):
    command = [GIT_PATH, "worktree", "remove", worktree_path]
    await run_command(command=command, target_path=target_path)


@tool("git-add-all-tool", description="Add all files to the git index in the target directory")
async def git_add_all(target_path: Path):
    command = [GIT_PATH, "add", "."]
    await run_command(command=command, target_path=target_path)


@tool("git-commit-tool", description="Make a git commit with a message in the target directory")
async def git_commit(target_path: Path, message: str):
    command = [GIT_PATH, "commit", "-m", message]
    await run_command(command=command, target_path=target_path)


@tool("git-push-tool", description="Make a git push in the target directory")
async def git_push(target_path: Path):
    command = [GIT_PATH, "push"]
    await run_command(command=command, target_path=target_path)


@tool("git-branch-delete-tool", description="Delete a git branch in the target directory")
async def git_branch_delete(target_path: Path, branch_name: str):
    command = [GIT_PATH, "branch", "-D", branch_name]
    await run_command(command=command, target_path=target_path)


async def git_cleanup(target_path: Path, worktree_path: Path, branch_name: str, *, is_error: bool):
    try:
        print_message("Removing worktree", style="heading")
        command = [GIT_PATH, "worktree", "remove", worktree_path]
        await run_command(command=command, target_path=target_path)
    except (RuntimeError, OSError) as error:
        print_message(f"Failed to remove worktree: {error}", style="error")

    if not is_error:
        return

    try:
        print_message("Deleting branch", style="heading")
        command = [GIT_PATH, "branch", "-D", branch_name]
        await run_command(command=command, target_path=target_path)
    except (RuntimeError, OSError) as error:
        print_message(f"Failed to delete branch: {error}", style="error")
