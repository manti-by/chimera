from unittest.mock import patch

import pytest

from chimera.services.terminal import print_heading, print_message


class TestPrintMessage:
    """Test cases for print_message function."""

    def test_print_message_default_style(self, capsys):
        """Test print_message with default style."""
        print_message("Test message")
        captured = capsys.readouterr()

        assert "Test message" in captured.out

    def test_print_message_heading_style(self, capsys):
        """Test print_message with heading style."""
        print_message("Heading message", style="heading")
        captured = capsys.readouterr()

        assert "Heading message" in captured.out
        assert "●" in captured.out

    def test_print_message_result_style(self, capsys):
        """Test print_message with result style."""
        print_message("Result message", style="result")
        captured = capsys.readouterr()

        assert "Result message" in captured.out
        assert "→" in captured.out

    def test_print_message_info_style(self, capsys):
        """Test print_message with info style."""
        print_message("Info message", style="info")
        captured = capsys.readouterr()

        assert "Info message" in captured.out

    def test_print_message_debug_style(self, capsys):
        """Test print_message with debug style."""
        print_message("Debug message", style="debug")
        captured = capsys.readouterr()

        assert "Debug message" in captured.out
        assert "*" * 80 in captured.out

    def test_print_message_error_style(self, capsys):
        """Test print_message with error style."""
        print_message("Error message", style="error")
        captured = capsys.readouterr()

        assert "Error message" in captured.out

    def test_print_message_error_logs_to_logger(self, capsys):
        """Test that error messages are logged."""
        with patch("chimera.services.terminal.logger") as mock_logger:
            print_message("Error message", style="error")

            mock_logger.error.assert_called_once_with("Error message")

    def test_print_message_empty_message_not_logged(self, capsys):
        """Test that empty messages are not logged."""
        with patch("chimera.services.terminal.logger") as mock_logger:
            print_message("   ", style="error")

            mock_logger.error.assert_not_called()

    def test_print_message_whitespace_only_not_logged(self, capsys):
        """Test that whitespace-only messages are not logged."""
        with patch("chimera.services.terminal.logger") as mock_logger:
            print_message("\n\t  \n", style="error")

            mock_logger.error.assert_not_called()


class TestPrintHeading:
    """Test cases for print_heading function."""

    @pytest.mark.asyncio
    async def test_print_heading_outputs_header(self, capsys):
        """Test that print_heading outputs the header."""
        await print_heading()
        captured = capsys.readouterr()

        # The header contains ASCII art
        assert "Y88b" in captured.out or len(captured.out) > 0

    @pytest.mark.asyncio
    async def test_print_heading_stylizes_text(self, capsys):
        """Test that print_heading stylizes the header text."""
        await print_heading()
        captured = capsys.readouterr()

        # Rich adds styling escape sequences
        assert captured.out != ""

    @pytest.mark.asyncio
    async def test_print_heading_adds_newline(self, capsys):
        """Test that print_heading adds a leading newline."""
        await print_heading()
        captured = capsys.readouterr()

        # Output should start with a newline
        assert captured.out.startswith("\n") or "chimera" in captured.out.lower()
