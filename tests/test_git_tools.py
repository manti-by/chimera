from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.tools.git import (
    git_add_all_tool,
    git_branch_delete_tool,
    git_commit_tool,
    git_pull_tool,
    git_push_tool,
    git_worktree_create_tool,
    git_worktree_remove_tool,
)


class TestGitWorktreeCreateTool:
    """Test cases for git_worktree_create_tool."""

    @pytest.mark.asyncio
    async def test_git_worktree_create_tool_returns_worktree_path(self, mock_path):
        """Test that git_worktree_create_tool returns the worktree path."""
        branch_name = "feature/test-branch"

        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git"), "worktree_path": mock_path}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.git.git_worktree_remove", new_callable=AsyncMock),
            patch("chimera.tools.git.git_branch_delete", new_callable=AsyncMock),
        ):
            mock_run.return_value = (0, "", "")

            result = await git_worktree_create_tool.ainvoke({"target_path": mock_path, "branch_name": branch_name})

        assert isinstance(result, Path)
        assert branch_name in str(result)

    @pytest.mark.asyncio
    async def test_git_worktree_create_tool_uses_git_worktree_add(self, mock_path):
        """Test that git_worktree_create_tool uses git worktree add command."""
        branch_name = "feature/test-branch"

        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git"), "worktree_path": mock_path}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.git.git_worktree_remove", new_callable=AsyncMock),
            patch("chimera.tools.git.git_branch_delete", new_callable=AsyncMock),
        ):
            mock_run.return_value = (0, "", "")

            await git_worktree_create_tool.ainvoke({"target_path": mock_path, "branch_name": branch_name})

        call_args = mock_run.call_args[1]["command"]
        assert "worktree" in call_args
        assert "add" in call_args
        assert "-b" in call_args
        assert branch_name in call_args

    @pytest.mark.asyncio
    async def test_git_worktree_create_tool_removes_existing_worktree(self, mock_path):
        """Test that git_worktree_create_tool removes existing worktree."""
        branch_name = "feature/test-branch"
        worktree_path = mock_path / branch_name

        # Create the worktree path to simulate existing worktree
        worktree_path.mkdir(parents=True, exist_ok=True)

        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git"), "worktree_path": mock_path}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.git.git_worktree_remove", new_callable=AsyncMock) as mock_remove,
            patch("chimera.tools.git.git_branch_delete", new_callable=AsyncMock) as mock_delete,
        ):
            mock_run.return_value = (0, "", "")

            await git_worktree_create_tool.ainvoke({"target_path": mock_path, "branch_name": branch_name})

        mock_remove.assert_called_once()
        mock_delete.assert_called_once()


class TestGitWorktreeRemoveTool:
    """Test cases for git_worktree_remove_tool."""

    @pytest.mark.asyncio
    async def test_git_worktree_remove_tool_calls_service(self, mock_path):
        """Test that git_worktree_remove_tool calls the service function."""
        worktree_path = mock_path / "worktree"

        with patch("chimera.tools.git.git_worktree_remove", new_callable=AsyncMock) as mock_remove:
            await git_worktree_remove_tool.ainvoke({"target_path": mock_path, "worktree_path": worktree_path})

        mock_remove.assert_called_once_with(mock_path, worktree_path, False)

    @pytest.mark.asyncio
    async def test_git_worktree_remove_tool_passes_force_parameter(self, mock_path):
        """Test that git_worktree_remove_tool passes force parameter."""
        worktree_path = mock_path / "worktree"

        with patch("chimera.tools.git.git_worktree_remove", new_callable=AsyncMock) as mock_remove:
            await git_worktree_remove_tool.ainvoke(
                {"target_path": mock_path, "worktree_path": worktree_path, "force": True}
            )

        mock_remove.assert_called_once_with(mock_path, worktree_path, True)


class TestGitAddAllTool:
    """Test cases for git_add_all_tool."""

    @pytest.mark.asyncio
    async def test_git_add_all_tool_uses_git_add(self, mock_path):
        """Test that git_add_all_tool uses git add command."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await git_add_all_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "add" in call_args
        assert "." in call_args


class TestGitCommitTool:
    """Test cases for git_commit_tool."""

    @pytest.mark.asyncio
    async def test_git_commit_tool_uses_git_commit(self, mock_path):
        """Test that git_commit_tool uses git commit command."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await git_commit_tool.ainvoke({"target_path": mock_path, "message": "Test commit message"})

        call_args = mock_run.call_args[1]["command"]
        assert "commit" in call_args
        assert "-m" in call_args
        assert "Test commit message" in call_args


class TestGitPullTool:
    """Test cases for git_pull_tool."""

    @pytest.mark.asyncio
    async def test_git_pull_tool_uses_git_pull(self, mock_path):
        """Test that git_pull_tool uses git pull command."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await git_pull_tool.ainvoke({"target_path": mock_path, "branch_name": "main"})

        call_args = mock_run.call_args[1]["command"]
        assert "pull" in call_args
        assert "origin" in call_args
        assert "main" in call_args

    @pytest.mark.asyncio
    async def test_git_pull_tool_uses_default_branch(self, mock_path):
        """Test that git_pull_tool uses default branch 'master'."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await git_pull_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "master" in call_args

    @pytest.mark.asyncio
    async def test_git_pull_tool_returns_true_on_success(self, mock_path):
        """Test that git_pull_tool returns True on success."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            result = await git_pull_tool.ainvoke({"target_path": mock_path})

        assert result is True

    @pytest.mark.asyncio
    async def test_git_pull_tool_returns_false_on_failure(self, mock_path):
        """Test that git_pull_tool returns False on failure."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (1, "", "error")

            result = await git_pull_tool.ainvoke({"target_path": mock_path})

        assert result is False


class TestGitPushTool:
    """Test cases for git_push_tool."""

    @pytest.mark.asyncio
    async def test_git_push_tool_uses_git_push(self, mock_path):
        """Test that git_push_tool uses git push command."""
        with (
            patch("chimera.tools.git.GIT", {"path": Path("/usr/bin/git")}),
            patch("chimera.tools.git.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await git_push_tool.ainvoke({"target_path": mock_path, "branch_name": "feature/test"})

        call_args = mock_run.call_args[1]["command"]
        assert "push" in call_args
        assert "--set-upstream" in call_args
        assert "origin" in call_args
        assert "feature/test" in call_args


class TestGitBranchDeleteTool:
    """Test cases for git_branch_delete_tool."""

    @pytest.mark.asyncio
    async def test_git_branch_delete_tool_calls_service(self, mock_path):
        """Test that git_branch_delete_tool calls the service function."""
        with patch("chimera.tools.git.git_branch_delete", new_callable=AsyncMock) as mock_delete:
            await git_branch_delete_tool.ainvoke({"target_path": mock_path, "branch_name": "feature/old-branch"})

        mock_delete.assert_called_once_with(mock_path, "feature/old-branch")
