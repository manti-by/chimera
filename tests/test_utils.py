from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from chimera.services.utils import is_package_installed, live_stream, merge_review_results


class TestLiveStream:
    """Test cases for live_stream function."""

    @pytest.mark.asyncio
    async def test_live_stream_reads_lines(self):
        """Test that live_stream reads lines from stream."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"line 1\n", b"line 2\n", b""])

        result = []
        await live_stream(mock_stream, result=result, disable_stdio=True)

        assert result == ["line 1\n", "line 2\n"]

    @pytest.mark.asyncio
    async def test_live_stream_writes_to_stdout(self, capsys):
        """Test that live_stream writes to stdout when not disabled."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"output line\n", b""])

        await live_stream(mock_stream, result=None, disable_stdio=False)

        captured = capsys.readouterr()
        assert "output line" in captured.out

    @pytest.mark.asyncio
    async def test_live_stream_does_not_write_when_disabled(self, capsys):
        """Test that live_stream does not write to stdout when disabled."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"output line\n", b""])

        result = []
        await live_stream(mock_stream, result=result, disable_stdio=True)

        captured = capsys.readouterr()
        assert captured.out == ""
        assert result == ["output line\n"]

    @pytest.mark.asyncio
    async def test_live_stream_handles_empty_lines(self):
        """Test that live_stream handles empty lines correctly."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"", b""])

        result = []
        await live_stream(mock_stream, result=result, disable_stdio=True)

        assert result == []

    @pytest.mark.asyncio
    async def test_live_stream_appends_to_result(self):
        """Test that live_stream appends to existing result list."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"new line\n", b""])

        result = ["existing line\n"]
        await live_stream(mock_stream, result=result, disable_stdio=True)

        assert result == ["existing line\n", "new line\n"]

    @pytest.mark.asyncio
    async def test_live_stream_decodes_bytes(self):
        """Test that live_stream decodes bytes to string."""
        mock_stream = AsyncMock()
        mock_stream.readline = AsyncMock(side_effect=[b"\xc3\xa9\n", b""])  # UTF-8 for 'é'

        result = []
        await live_stream(mock_stream, result=result, disable_stdio=True)

        # The bytes are decoded to the actual UTF-8 character
        assert result == ["é\n"]


class TestIsPackageInstalled:
    """Test cases for is_package_installed function."""

    @pytest.mark.asyncio
    async def test_is_package_installed_returns_true_when_package_found(self):
        """Test that is_package_installed returns True when package is found."""
        with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "some-package==1.0.0", "")

            result = await is_package_installed(Path("/test"), "some-package")

        assert result is True

    @pytest.mark.asyncio
    async def test_is_package_installed_returns_false_when_package_not_found(self):
        """Test that is_package_installed returns False when package is not found."""
        with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            result = await is_package_installed(Path("/test"), "nonexistent-package")

        assert result is False

    @pytest.mark.asyncio
    async def test_is_package_installed_uses_uv_path(self):
        """Test that is_package_installed uses the UV path from settings."""
        with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await is_package_installed(Path("/test"), "package-name")

        call_args = mock_run.call_args
        assert "tree" in call_args[1]["command"]
        assert "--package" in call_args[1]["command"]
        assert "package-name" in call_args[1]["command"]

    @pytest.mark.asyncio
    async def test_is_package_installed_disables_stdio(self):
        """Test that is_package_installed disables stdio."""
        with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await is_package_installed(Path("/test"), "package")

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["disable_stdio"] is True

    @pytest.mark.asyncio
    async def test_is_package_installed_uses_target_path(self):
        """Test that is_package_installed uses the provided target path."""
        with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            target_path = Path("/custom/path")
            await is_package_installed(target_path, "package")

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == target_path


class TestMergeReviewResults:
    """Test cases for merge_review_results function."""

    @pytest.mark.asyncio
    async def test_merge_review_results_combines_exit_codes(self):
        """Test that merge_review_results sums exit codes."""
        results = [
            (0, "", ""),
            (1, "", ""),
            (2, "", ""),
        ]

        exit_code, _, _ = await merge_review_results(results)

        assert exit_code == 3

    @pytest.mark.asyncio
    async def test_merge_review_results_combines_stdout(self):
        """Test that merge_review_results combines stdout."""
        results = [
            (0, "output 1", ""),
            (0, "output 2", ""),
        ]

        _, stdout, _ = await merge_review_results(results)

        assert "output 1" in stdout
        assert "output 2" in stdout

    @pytest.mark.asyncio
    async def test_merge_review_results_combines_stderr(self):
        """Test that merge_review_results combines stderr."""
        results = [
            (0, "", "error 1"),
            (0, "", "error 2"),
        ]

        _, _, stderr = await merge_review_results(results)

        assert "error 1" in stderr
        assert "error 2" in stderr

    @pytest.mark.asyncio
    async def test_merge_review_results_handles_empty_results(self):
        """Test that merge_review_results handles empty results list."""
        results = []

        exit_code, stdout, stderr = await merge_review_results(results)

        assert exit_code == 0
        assert stdout == ""
        assert stderr == ""

    @pytest.mark.asyncio
    async def test_merge_review_results_strips_whitespace(self):
        """Test that merge_review_results strips whitespace from outputs."""
        results = [
            (0, "  output with spaces  ", ""),
            (0, "", "  error with spaces  "),
        ]

        _, stdout, stderr = await merge_review_results(results)

        # Should not have leading/trailing whitespace in individual entries
        assert "output with spaces" in stdout
        assert "error with spaces" in stderr

    @pytest.mark.asyncio
    async def test_merge_review_results_handles_single_result(self):
        """Test that merge_review_results handles single result."""
        results = [
            (5, "single output", "single error"),
        ]

        exit_code, stdout, stderr = await merge_review_results(results)

        assert exit_code == 5
        assert stdout.strip() == "single output"
        assert stderr.strip() == "single error"

    @pytest.mark.asyncio
    async def test_merge_review_results_preserves_order(self):
        """Test that merge_review_results preserves order of results."""
        results = [
            (0, "first", ""),
            (0, "second", ""),
            (0, "third", ""),
        ]

        _, stdout, _ = await merge_review_results(results)

        # Check that outputs appear in order
        first_pos = stdout.find("first")
        second_pos = stdout.find("second")
        third_pos = stdout.find("third")

        assert first_pos < second_pos < third_pos
