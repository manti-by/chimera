import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.services.opencode import (
    get_opencode_session_id,
    get_opencode_sessions,
    run_opencode_agent,
)


class TestRunOpencodeAgent:
    """Test cases for run_opencode_agent function."""

    @pytest.mark.asyncio
    async def test_run_opencode_agent_basic_call(self):
        """Test basic call to run_opencode_agent."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "success", "")

            result = await run_opencode_agent(
                target_path=Path("/test"),
                task="Test task",
                model="test-model",
                agent="test-agent",
            )

        assert result == (0, "success", "")

    @pytest.mark.asyncio
    async def test_run_opencode_agent_builds_correct_command(self):
        """Test that run_opencode_agent builds the correct command."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await run_opencode_agent(
                target_path=Path("/test"),
                task="Test task",
                model="test-model",
                agent="test-agent",
            )

        call_args = mock_run.call_args[1]["command"]
        assert "run" in call_args
        assert "--model" in call_args
        assert "test-model" in call_args
        assert "--agent" in call_args
        assert "test-agent" in call_args

    @pytest.mark.asyncio
    async def test_run_opencode_agent_includes_session_id(self):
        """Test that run_opencode_agent includes session ID when provided."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await run_opencode_agent(
                target_path=Path("/test"),
                task="Test task",
                model="test-model",
                agent="test-agent",
                session_id="test-session-id",
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--session" in call_args
        assert "test-session-id" in call_args

    @pytest.mark.asyncio
    async def test_run_opencode_agent_includes_task_title(self):
        """Test that run_opencode_agent includes task title when provided."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await run_opencode_agent(
                target_path=Path("/test"),
                task="Test task",
                model="test-model",
                agent="test-agent",
                task_title="Test Title",
            )

        call_args = mock_run.call_args[1]["command"]
        assert "--title" in call_args
        assert "Test Title" in call_args

    @pytest.mark.asyncio
    async def test_run_opencode_agent_uses_target_path(self):
        """Test that run_opencode_agent uses the target path."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            target_path = Path("/custom/path")
            await run_opencode_agent(
                target_path=target_path,
                task="Test task",
                model="test-model",
                agent="test-agent",
            )

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == target_path

    @pytest.mark.asyncio
    async def test_run_opencode_agent_passes_disable_stdio(self):
        """Test that run_opencode_agent passes disable_stdio parameter."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await run_opencode_agent(
                target_path=Path("/test"),
                task="Test task",
                model="test-model",
                agent="test-agent",
                disable_stdio=True,
            )

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["disable_stdio"] is True

    @pytest.mark.asyncio
    async def test_run_opencode_agent_quotes_task(self):
        """Test that run_opencode_agent quotes the task argument."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await run_opencode_agent(
                target_path=Path("/test"),
                task="task with spaces and 'quotes'",
                model="test-model",
                agent="test-agent",
            )

        call_args = mock_run.call_args[1]["command"]
        # The last argument should be the quoted task
        task_arg = call_args[-1]
        assert "task" in task_arg

    @pytest.mark.asyncio
    async def test_run_opencode_agent_truncates_long_task(self):
        """Test that run_opencode_agent truncates tasks longer than 4095 characters."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            long_task = "a" * 5000
            await run_opencode_agent(
                target_path=Path("/test"),
                task=long_task,
                model="test-model",
                agent="test-agent",
            )

        call_args = mock_run.call_args[1]["command"]
        task_arg = call_args[-1]
        assert len(task_arg) <= 4095


class TestGetOpencodeSessions:
    """Test cases for get_opencode_sessions function."""

    @pytest.mark.asyncio
    async def test_get_opencode_sessions_parses_json(self):
        """Test that get_opencode_sessions parses JSON output."""
        sessions_data = [
            {"id": "session-1", "title": "Test 1"},
            {"id": "session-2", "title": "Test 2"},
        ]

        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, json.dumps(sessions_data), "")

            result = await get_opencode_sessions(Path("/test"))

        assert result == sessions_data

    @pytest.mark.asyncio
    async def test_get_opencode_sessions_uses_session_list_command(self):
        """Test that get_opencode_sessions uses the session list command."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "[]", "")

            await get_opencode_sessions(Path("/test"))

        call_args = mock_run.call_args[1]["command"]
        assert "session" in call_args
        assert "list" in call_args
        assert "--format" in call_args
        assert "json" in call_args

    @pytest.mark.asyncio
    async def test_get_opencode_sessions_disables_stdio(self):
        """Test that get_opencode_sessions disables stdio."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "[]", "")

            await get_opencode_sessions(Path("/test"))

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["disable_stdio"] is True

    @pytest.mark.asyncio
    async def test_get_opencode_sessions_returns_empty_list_on_empty_output(self):
        """Test that get_opencode_sessions returns empty list on empty output."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            with pytest.raises(json.JSONDecodeError):
                await get_opencode_sessions(Path("/test"))

    @pytest.mark.asyncio
    async def test_get_opencode_sessions_uses_target_path(self):
        """Test that get_opencode_sessions uses the target path."""
        with patch("chimera.services.opencode.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "[]", "")

            target_path = Path("/custom/path")
            await get_opencode_sessions(target_path)

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == target_path


class TestGetOpencodeSessionId:
    """Test cases for get_opencode_session_id function."""

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_finds_matching_session(self):
        """Test that get_opencode_session_id finds a matching session."""
        sessions_data = [
            {
                "id": "session-123",
                "title": "Test Session",
                "directory": "/test/path",
                "updated": "2024-01-01T00:00:00Z",
            },
        ]

        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sessions_data

            result = await get_opencode_session_id(Path("/test/path"), "Test Session")

        assert result == "session-123"

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_returns_none_when_no_match(self):
        """Test that get_opencode_session_id returns None when no session matches."""
        sessions_data = [
            {
                "id": "session-123",
                "title": "Different Session",
                "directory": "/test/path",
                "updated": "2024-01-01T00:00:00Z",
            },
        ]

        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sessions_data

            result = await get_opencode_session_id(Path("/test/path"), "Test Session")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_checks_directory(self):
        """Test that get_opencode_session_id checks directory matches."""
        sessions_data = [
            {
                "id": "session-123",
                "title": "Test Session",
                "directory": "/different/path",
                "updated": "2024-01-01T00:00:00Z",
            },
        ]

        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sessions_data

            result = await get_opencode_session_id(Path("/test/path"), "Test Session")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_sorts_by_updated(self):
        """Test that get_opencode_session_id sorts by updated date (newest first)."""
        sessions_data = [
            {
                "id": "session-old",
                "title": "Test Session",
                "directory": "/test/path",
                "updated": "2024-01-01T00:00:00Z",
            },
            {
                "id": "session-new",
                "title": "Test Session",
                "directory": "/test/path",
                "updated": "2024-01-02T00:00:00Z",
            },
        ]

        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = sessions_data

            result = await get_opencode_session_id(Path("/test/path"), "Test Session")

        assert result == "session-new"

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_returns_none_on_empty_sessions(self):
        """Test that get_opencode_session_id returns None when sessions list is empty."""
        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []

            result = await get_opencode_session_id(Path("/test/path"), "Test Session")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_opencode_session_id_uses_target_path(self):
        """Test that get_opencode_session_id passes target_path to get_opencode_sessions."""
        with patch("chimera.services.opencode.get_opencode_sessions", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []

            target_path = Path("/custom/path")
            await get_opencode_session_id(target_path, "Test Session")

        call_kwargs = mock_get.call_args.kwargs
        assert call_kwargs["target_path"] == target_path
