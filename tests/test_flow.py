from unittest.mock import patch

import pytest

from chimera.services.flow import user_input


class TestUserInput:
    """Test cases for user_input function."""

    @pytest.mark.asyncio
    async def test_user_input_returns_choice(self, capsys):
        """Test that user_input returns the selected choice."""
        options = [("1", "Option 1"), ("2", "Option 2")]

        with patch("builtins.input", return_value="1"):
            action, comment = await user_input(options)

        assert action == "Option 1"
        assert comment is None

    @pytest.mark.asyncio
    async def test_user_input_returns_comment_for_comment_action(self, capsys):
        """Test that user_input returns comment when action is 'comment'."""
        options = [("1", "Option 1"), ("2", "comment")]

        with patch("builtins.input", side_effect=["2", "Test comment"]):
            action, comment = await user_input(options)

        assert action == "comment"
        assert comment == "Test comment"

    @pytest.mark.asyncio
    async def test_user_input_prompts_for_comment_until_not_empty(self, capsys):
        """Test that user_input prompts for comment until non-empty input."""
        options = [("1", "comment")]

        with patch("builtins.input", side_effect=["1", "", "   ", "Final comment"]):
            action, comment = await user_input(options)

        assert action == "comment"
        assert comment == "Final comment"

    @pytest.mark.asyncio
    async def test_user_input_uses_default_for_empty_input(self, capsys):
        """Test that user_input uses default option for empty input."""
        options = [("1", "Default Option"), ("2", "Option 2")]

        with patch("builtins.input", return_value=""):
            action, _ = await user_input(options)

        assert action == "Default Option"

    @pytest.mark.asyncio
    async def test_user_input_rejects_invalid_choice(self, capsys):
        """Test that user_input rejects invalid choices."""
        options = [("1", "Option 1")]

        with patch("builtins.input", side_effect=["invalid", "1"]):
            action, _ = await user_input(options)

        assert action == "Option 1"

    @pytest.mark.asyncio
    async def test_user_input_prints_options(self, capsys):
        """Test that user_input prints available options."""
        options = [("1", "Option 1"), ("2", "Option 2")]

        with patch("builtins.input", return_value="1"):
            await user_input(options)

        captured = capsys.readouterr()
        assert "How would you like to proceed?" in captured.out
        assert "[1] Option 1" in captured.out
        assert "[2] Option 2" in captured.out

    @pytest.mark.asyncio
    async def test_user_input_marks_default_option(self, capsys):
        """Test that user_input marks the default option."""
        options = [("1", "Option 1"), ("2", "Option 2")]

        with patch("builtins.input", return_value="1"):
            await user_input(options)

        captured = capsys.readouterr()
        assert "default" in captured.out

    @pytest.mark.asyncio
    async def test_user_input_handles_case_insensitive_input(self, capsys):
        """Test that user_input handles case-insensitive input."""
        options = [("a", "Option A"), ("b", "Option B")]

        with patch("builtins.input", return_value="A"):
            action, _ = await user_input(options)

        assert action == "Option A"

    @pytest.mark.asyncio
    async def test_user_input_strips_whitespace(self, capsys):
        """Test that user_input strips whitespace from input."""
        options = [("1", "Option 1")]

        with patch("builtins.input", return_value="  1  "):
            action, _ = await user_input(options)

        assert action == "Option 1"
