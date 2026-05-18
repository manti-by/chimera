import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from chimera.services.subprocess import run_command


class TestSubprocessService:
    """Test cases for subprocess service."""

    @pytest.mark.asyncio
    async def test_run_command_returns_exit_code_stdout_stderr(self, mock_process):
        """Test that run_command returns exit code, stdout, and stderr."""
        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", new_callable=AsyncMock),
        ):
            mock_create.return_value = mock_process
            exit_code, stdout, stderr = await run_command(["cmd"], Path("/test"))

        assert exit_code == 0
        assert isinstance(stdout, str)
        assert isinstance(stderr, str)

    @pytest.mark.asyncio
    async def test_run_command_uses_correct_cwd(self, mock_process):
        """Test that run_command uses the correct working directory."""
        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", new_callable=AsyncMock),
        ):
            mock_create.return_value = mock_process
            await run_command(["cmd"], Path("/custom/path"))

        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs["cwd"] == Path("/custom/path")

    @pytest.mark.asyncio
    async def test_run_command_pipes_stdout_stderr(self, mock_process):
        """Test that run_command pipes stdout and stderr."""
        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", new_callable=AsyncMock),
        ):
            mock_create.return_value = mock_process
            await run_command(["cmd"], Path("/test"))

        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs["stdout"] == asyncio.subprocess.PIPE
        assert call_kwargs["stderr"] == asyncio.subprocess.PIPE

    @pytest.mark.asyncio
    async def test_run_command_with_command_list(self, mock_process):
        """Test that run_command accepts a list of command arguments."""
        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", new_callable=AsyncMock),
        ):
            mock_create.return_value = mock_process
            await run_command(["git", "status", "--short"], Path("/test"))

        call_args = mock_create.call_args.args
        assert call_args == ("git", "status", "--short")

    @pytest.mark.asyncio
    async def test_run_command_with_disable_stdio(self, mock_process):
        """Test that run_command passes disable_stdio to live_stream."""
        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream") as mock_stream,
        ):
            mock_create.return_value = mock_process
            await run_command(["cmd"], Path("/test"), disable_stdio=True)

        # Check that live_stream was called with disable_stdio=True
        calls = mock_stream.call_args_list
        assert len(calls) == 2  # Called for stdout and stderr
        for call in calls:
            assert call.kwargs.get("disable_stdio") is True

    @pytest.mark.asyncio
    async def test_run_command_handles_failure(self, mock_process_failure):
        """Test that run_command handles command failure correctly."""

        async def capture_stream(stream, result=None, disable_stdio=False):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode()
                if result is not None:
                    result.append(decoded)

        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", side_effect=capture_stream),
        ):
            mock_create.return_value = mock_process_failure
            exit_code, _, stderr = await run_command(["cmd"], Path("/test"))

        assert exit_code == 1
        assert "error message" in stderr

    @pytest.mark.asyncio
    async def test_run_command_kills_process_on_none_streams(self):
        """Test that run_command kills process if stdout/stderr is None."""
        mock_proc = MagicMock()
        mock_proc.stdout = None
        mock_proc.stderr = None
        mock_proc.kill = MagicMock()

        with patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = mock_proc

            with pytest.raises(AttributeError, match="stdout/stderr is None"):
                await run_command(["cmd"], Path("/test"))

        mock_proc.kill.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_command_returns_combined_output(self):
        """Test that run_command combines output from live_stream."""

        async def capture_stream(stream, result=None, disable_stdio=False):
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode()
                if result is not None:
                    result.append(decoded)

        mock_stdout = AsyncMock()
        mock_stdout.readline = AsyncMock(side_effect=[b"line 1\n", b"line 2\n", b""])

        mock_stderr = AsyncMock()
        mock_stderr.readline = AsyncMock(side_effect=[b"error 1\n", b""])

        mock_proc = MagicMock()
        mock_proc.stdout = mock_stdout
        mock_proc.stderr = mock_stderr
        mock_proc.kill = MagicMock()
        mock_proc.wait = AsyncMock(return_value=0)

        with (
            patch("asyncio.create_subprocess_exec", new_callable=AsyncMock) as mock_create,
            patch("chimera.services.subprocess.live_stream", side_effect=capture_stream),
        ):
            mock_create.return_value = mock_proc
            exit_code, stdout, stderr = await run_command(["cmd"], Path("/test"))

        assert "line 1" in stdout
        assert "line 2" in stdout
        assert exit_code == 0
        assert stderr == "error 1\n"
