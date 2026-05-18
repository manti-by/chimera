from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.tools.test import pytest_tool


class TestPytestTool:
    """Test cases for pytest_tool."""

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_uv_run(self, mock_path):
        """Test that pytest_tool uses uv run command."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "run" in call_args
        assert "--active" in call_args

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_pytest(self, mock_path):
        """Test that pytest_tool uses pytest command."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "pytest" in call_args

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_last_failed_flag(self, mock_path):
        """Test that pytest_tool uses --lf (last-failed) flag."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "--lf" in call_args

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_quiet_flag(self, mock_path):
        """Test that pytest_tool uses --quiet flag."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "--quiet" in call_args

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_no_color_flag(self, mock_path):
        """Test that pytest_tool uses --color=no flag."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_args = mock_run.call_args[1]["command"]
        assert "--color=no" in call_args

    @pytest.mark.asyncio
    async def test_pytest_tool_returns_command_result(self, mock_path):
        """Test that pytest_tool returns the command result."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "2 passed", "")

            result = await pytest_tool.ainvoke({"target_path": mock_path})

        assert result == (0, "2 passed", "")

    @pytest.mark.asyncio
    async def test_pytest_tool_returns_failure_result(self, mock_path):
        """Test that pytest_tool returns failure result on test failures."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (1, "", "1 failed")

            result = await pytest_tool.ainvoke({"target_path": mock_path})

        assert result == (1, "", "1 failed")

    @pytest.mark.asyncio
    async def test_pytest_tool_uses_target_path(self, mock_path):
        """Test that pytest_tool uses the target path."""
        with (
            patch("chimera.tools.test.UV", {"path": Path("/usr/bin/uv")}),
            patch("chimera.tools.test.run_command", new_callable=AsyncMock) as mock_run,
        ):
            mock_run.return_value = (0, "", "")

            await pytest_tool.ainvoke({"target_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == mock_path
