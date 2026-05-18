from unittest.mock import AsyncMock, patch

import pytest

from chimera.services.prompt import get_prompt


class TestGetPrompt:
    """Test cases for get_prompt function."""

    @pytest.mark.asyncio
    async def test_get_prompt_reads_file(self, tmp_path):
        """Test that get_prompt reads the prompt file."""
        prompt_content = "This is a test prompt."

        with (
            patch("chimera.services.prompt.aiofiles.open") as mock_open,
            patch("chimera.services.prompt.BASE_PATH", tmp_path),
        ):
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=prompt_content)
            mock_open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
            mock_open.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await get_prompt("test_prompt")

        assert result == prompt_content

    @pytest.mark.asyncio
    async def test_get_prompt_formats_with_kwargs(self, tmp_path):
        """Test that get_prompt formats the prompt with kwargs."""
        prompt_content = "Hello {user}!"

        with (
            patch("chimera.services.prompt.aiofiles.open") as mock_open,
            patch("chimera.services.prompt.BASE_PATH", tmp_path),
        ):
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=prompt_content)
            mock_open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
            mock_open.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await get_prompt("test_prompt", user="World")

        assert result == "Hello World!"

    @pytest.mark.asyncio
    async def test_get_prompt_uses_correct_path(self, tmp_path):
        """Test that get_prompt uses the correct file path."""
        prompt_name = "system/build_agent"
        expected_path = tmp_path / f"chimera/prompts/{prompt_name}.md"

        with (
            patch("chimera.services.prompt.aiofiles.open") as mock_open,
            patch("chimera.services.prompt.BASE_PATH", tmp_path),
        ):
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value="content")
            mock_open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
            mock_open.return_value.__aexit__ = AsyncMock(return_value=False)

            await get_prompt(prompt_name)

        mock_open.assert_called_once()
        call_args = mock_open.call_args[0]
        assert str(expected_path) in str(call_args[0])

    @pytest.mark.asyncio
    async def test_get_prompt_returns_unformatted_content_without_kwargs(self, tmp_path):
        """Test that get_prompt returns unformatted content when no kwargs provided."""
        prompt_content = "Plain content without placeholders"

        with (
            patch("chimera.services.prompt.aiofiles.open") as mock_open,
            patch("chimera.services.prompt.BASE_PATH", tmp_path),
        ):
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=prompt_content)
            mock_open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
            mock_open.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await get_prompt("test_prompt")

        assert result == prompt_content

    @pytest.mark.asyncio
    async def test_get_prompt_handles_multiple_placeholders(self, tmp_path):
        """Test that get_prompt handles multiple placeholders."""
        prompt_content = "{greeting} {user}! Today is {day}."

        with (
            patch("chimera.services.prompt.aiofiles.open") as mock_open,
            patch("chimera.services.prompt.BASE_PATH", tmp_path),
        ):
            mock_file = AsyncMock()
            mock_file.read = AsyncMock(return_value=prompt_content)
            mock_open.return_value.__aenter__ = AsyncMock(return_value=mock_file)
            mock_open.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await get_prompt("test_prompt", greeting="Hello", user="User", day="Monday")

        assert result == "Hello User! Today is Monday."
