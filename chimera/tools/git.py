from pathlib import Path

from langchain.tools import tool

from chimera.services.git import git_branch_delete, git_worktree_remove
from chimera.services.subprocess import run_command
from chimera.settings import GIT


@tool("git-worktree-create-tool", description="Create a git worktree from the target directory")
async def git_worktree_create_tool(target_path: Path, branch_name: str) -> Path:
    worktree_path = GIT["worktree_path"] / branch_name
    if worktree_path.exists():
        await git_worktree_remove(target_path=target_path, worktree_path=worktree_path, force=True)
        await git_branch_delete(target_path=target_path, branch_name=branch_name)

    command = [str(GIT["path"]), "worktree", "add", "-b", branch_name, str(worktree_path)]
    await run_command(command=command, target_path=target_path)
    return worktree_path


@tool("git-worktree-remove-tool", description="Remove a git worktree from the target directory")
async def git_worktree_remove_tool(target_path: Path, worktree_path: Path, force: bool = False):
    await git_worktree_remove(target_path, worktree_path, force)


@tool("git-add-all-tool", description="Add all files to the git index in the target directory")
async def git_add_all_tool(target_path: Path):
    command = [str(GIT["path"]), "add", "."]
    await run_command(command=command, target_path=target_path)


@tool("git-commit-tool", description="Make a git commit with a message in the target directory")
async def git_commit_tool(target_path: Path, message: str):
    command = [str(GIT["path"]), "commit", "-m", message]
    await run_command(command=command, target_path=target_path)


@tool("git-pull-tool", description="Pull from a remote branch in the target directory")
async def git_pull_tool(target_path: Path, branch_name: str = "master") -> bool:
    command = [str(GIT["path"]), "pull", "origin", branch_name]
    exit_code, _, _ = await run_command(command=command, target_path=target_path)
    return not exit_code


@tool("git-push-tool", description="Push to a remote branch in the target directory")
async def git_push_tool(target_path: Path, branch_name: str):
    command = [str(GIT["path"]), "push", "--set-upstream", "origin", branch_name]
    await run_command(command=command, target_path=target_path)


@tool("git-branch-delete-tool", description="Delete a git branch in the target directory")
async def git_branch_delete_tool(target_path: Path, branch_name: str):
    await git_branch_delete(target_path, branch_name)
