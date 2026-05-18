from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.tools.github import create_pull_request


class TestCreatePullRequest:
    """Test cases for create_pull_request tool."""

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_gh_pr_create(self, mock_path):
        """Test that create_pull_request uses gh pr create command."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "pr" in call_args
        assert "create" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_base_parameter(self, mock_path):
        """Test that create_pull_request uses base parameter."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR", "base": "develop"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--base" in call_args
        assert "develop" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_default_base(self, mock_path):
        """Test that create_pull_request uses default base 'master'."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--base" in call_args
        assert "master" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_head_parameter(self, mock_path):
        """Test that create_pull_request uses head parameter."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--head" in call_args
        assert "feature/test" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_title_parameter(self, mock_path):
        """Test that create_pull_request uses title parameter."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "My PR Title"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--title" in call_args
        assert "My PR Title" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_empty_body(self, mock_path):
        """Test that create_pull_request uses empty body."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--body" in call_args
        assert "" in call_args

    @pytest.mark.asyncio
    async def test_create_pull_request_returns_true_on_success(self, mock_path):
        """Test that create_pull_request returns True on success."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            result = await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        assert result is True

    @pytest.mark.asyncio
    async def test_create_pull_request_returns_false_on_failure(self, mock_path):
        """Test that create_pull_request returns False on failure."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (1, "", "error")

            result = await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        assert result is False

    @pytest.mark.asyncio
    async def test_create_pull_request_uses_target_path(self, mock_path):
        """Test that create_pull_request uses the target path."""
        with (
            patch("chimera.tools.github.GITHUB", {"path": Path("/usr/bin/gh")}),
            patch("chimera.tools.github.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await create_pull_request.ainvoke(
                {"target_path": mock_path, "branch_name": "feature/test", "title": "Test PR"}
            )

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == mock_path
