import pytest

from chimera.tools import (
    PLAN_HAS_QUESTIONS,
    PLAN_IS_READY_STRING,
    build_agent_tool,
    create_pull_request,
    get_available_tools,
    git_add_all_tool,
    git_branch_delete_tool,
    git_commit_tool,
    git_pull_tool,
    git_push_tool,
    git_worktree_create_tool,
    git_worktree_remove_tool,
    plan_agent_tool,
    pytest_tool,
    review_agents_tool,
    run_ruff_checks,
    run_ruff_format,
)


class TestToolsExports:
    """Test cases for tools module exports."""

    def test_git_tools_are_exported(self):
        """Test that all git tools are exported."""
        assert git_worktree_create_tool is not None
        assert git_worktree_remove_tool is not None
        assert git_add_all_tool is not None
        assert git_commit_tool is not None
        assert git_pull_tool is not None
        assert git_push_tool is not None
        assert git_branch_delete_tool is not None

    def test_github_tool_is_exported(self):
        """Test that github tool is exported."""
        assert create_pull_request is not None

    def test_lint_tools_are_exported(self):
        """Test that lint tools are exported."""
        assert run_ruff_format is not None
        assert run_ruff_checks is not None

    def test_opencode_tools_are_exported(self):
        """Test that opencode tools are exported."""
        assert plan_agent_tool is not None
        assert build_agent_tool is not None
        assert review_agents_tool is not None

    def test_test_tool_is_exported(self):
        """Test that test tool is exported."""
        assert pytest_tool is not None

    def test_constants_are_exported(self):
        """Test that constants are exported."""
        assert PLAN_IS_READY_STRING is not None
        assert PLAN_HAS_QUESTIONS is not None


class TestGetAvailableTools:
    """Test cases for get_available_tools function."""

    @pytest.mark.asyncio
    async def test_get_available_tools_returns_list(self):
        """Test that get_available_tools returns a list."""
        tools = await get_available_tools()

        assert isinstance(tools, list)

    @pytest.mark.asyncio
    async def test_get_available_tools_returns_all_tools(self):
        """Test that get_available_tools returns all expected tools."""
        tools = await get_available_tools()

        # Should have at least these tools
        assert len(tools) >= 11

        # Check that all expected tools are present
        _ = [t.name if hasattr(t, "name") else str(t) for t in tools]
        assert any("git-worktree-create" in str(t) for t in tools)
        assert any("git-worktree-remove" in str(t) for t in tools)
        assert any("git-add-all" in str(t) for t in tools)
        assert any("git-commit" in str(t) for t in tools)
        assert any("git-pull" in str(t) for t in tools)
        assert any("git-push" in str(t) for t in tools)
        assert any("git-branch-delete" in str(t) for t in tools)
        assert any("github-create-pull-request" in str(t) for t in tools)
        assert any("ruff-format" in str(t) for t in tools)
        assert any("ruff-lint" in str(t) for t in tools)
        assert any("plan-agent" in str(t) for t in tools)
        assert any("build-agent" in str(t) for t in tools)
        assert any("review-agents" in str(t) for t in tools)
        assert any("pytest" in str(t) for t in tools)
