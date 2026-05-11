from pathlib import Path

from chimera.services.subprocess import run_command
from chimera.services.terminal import print_message
from chimera.settings import GIT


async def git_worktree_remove(target_path: Path, worktree_path: Path, force: bool = False):
    command = [str(GIT["path"]), "worktree", "remove", str(worktree_path)]
    if force:
        command.append("--force")
    await run_command(command=command, target_path=target_path)


async def git_branch_delete(target_path: Path, branch_name: str):
    command = [str(GIT["path"]), "branch", "-D", branch_name]
    await run_command(command=command, target_path=target_path)


async def git_cleanup(target_path: Path, worktree_path: Path, branch_name: str, *, is_error: bool):
    try:
        print_message("Removing worktree", style="heading")
        await git_worktree_remove(target_path=target_path, worktree_path=worktree_path, force=is_error)
    except (OSError, RuntimeError) as error:
        print_message(f"Failed to remove worktree: {error}", style="error")

    if not is_error:
        return

    try:
        print_message("Deleting branch", style="heading")
        await git_branch_delete(target_path=target_path, branch_name=branch_name)
    except (OSError, RuntimeError) as error:
        print_message(f"Failed to delete branch: {error}", style="error")
