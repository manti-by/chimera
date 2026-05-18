from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.tools.lint import run_ruff_checks, run_ruff_format


class TestRunRuffFormat:
    """Test cases for run_ruff_format tool."""

    @pytest.mark.asyncio
    async def test_run_ruff_format_uses_uv_run(self, mock_path):
        """Test that run_ruff_format uses uv run command."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_format.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "run" in call_args
        assert "--active" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_format_uses_ruff_format(self, mock_path):
        """Test that run_ruff_format uses ruff format command."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_format.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "ruff" in call_args
        assert "format" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_format_uses_silent_flag(self, mock_path):
        """Test that run_ruff_format uses --silent flag."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_format.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "--silent" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_format_returns_command_result(self, mock_path):
        """Test that run_ruff_format returns the command result."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "formatted", "")

            result = await run_ruff_format.ainvoke({"target_path": mock_path})

        assert result == (0, "formatted", "")

    @pytest.mark.asyncio
    async def test_run_ruff_format_uses_target_path(self, mock_path):
        """Test that run_ruff_format uses the target path."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_format.ainvoke({"target_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == mock_path


class TestRunRuffChecks:
    """Test cases for run_ruff_checks tool."""

    @pytest.mark.asyncio
    async def test_run_ruff_checks_uses_uv_run(self, mock_path):
        """Test that run_ruff_checks uses uv run command."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "run" in call_args
        assert "--active" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_checks_uses_ruff_check(self, mock_path):
        """Test that run_ruff_checks uses ruff check command."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "ruff" in call_args
        assert "check" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_checks_uses_quiet_flag(self, mock_path):
        """Test that run_ruff_checks uses --quiet flag."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "--quiet" in call_args

    @pytest.mark.asyncio
    async def test_run_ruff_checks_returns_command_result(self, mock_path):
        """Test that run_ruff_checks returns the command result."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (1, "", "errors found")

            result = await run_ruff_checks.ainvoke({"target_path": mock_path})

        assert result == (1, "", "errors found")

    @pytest.mark.asyncio
    async def test_run_ruff_checks_uses_target_path(self, mock_path):
        """Test that run_ruff_checks uses the target path."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == mock_path

    @pytest.mark.asyncio
    async def test_run_ruff_checks_accepts_session_id(self, mock_path):
        """Test that run_ruff_checks accepts optional session_id parameter."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path, "session_id": "test-session"})

        # session_id is accepted but not used in the command
        mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_ruff_checks_works_without_session_id(self, mock_path):
        """Test that run_ruff_checks works without session_id parameter."""
        with (
            patch("chimera.tools.lint.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.lint.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await run_ruff_checks.ainvoke({"target_path": mock_path})

        mock_run.assert_called_once()
