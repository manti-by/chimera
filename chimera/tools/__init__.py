from .git import (
    git_add_all_tool,
    git_branch_delete_tool,
    git_commit_tool,
    git_pull_tool,
    git_push_tool,
    git_worktree_create_tool,
    git_worktree_remove_tool,
)
from .github import create_pull_request
from .lint import run_ruff_checks, run_ruff_format
from .opencode import build_agent_tool, plan_agent_tool, review_agents_tool
from .test import pytest_tool


async def get_available_tools() -> list:
    return [
        git_worktree_create_tool,
        git_worktree_remove_tool,
        git_add_all_tool,
        git_commit_tool,
        git_pull_tool,
        git_push_tool,
        git_branch_delete_tool,
        create_pull_request,
        run_ruff_format,
        run_ruff_checks,
        plan_agent_tool,
        build_agent_tool,
        review_agents_tool,
        pytest_tool,
    ]
