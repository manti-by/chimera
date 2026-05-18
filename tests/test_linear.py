from unittest.mock import patch

import pytest

from chimera.library.exceptions import LinearApiKeyException
from chimera.services.linear import get_linear_mcp_config


class TestLinearService:
    """Test cases for linear service functions."""

    def test_get_linear_mcp_config_with_valid_api_key(self, mock_linear_api_key):
        """Test get_linear_mcp_config returns correct config with valid API key."""
        with patch("chimera.services.linear.LINEAR", {"api_key": mock_linear_api_key}):
            config = get_linear_mcp_config()

        assert config["transport"] == "http"
        assert config["url"] == "https://mcp.linear.app/mcp"
        assert "Authorization" in config["headers"]
        assert mock_linear_api_key in config["headers"]["Authorization"]
        assert config["headers"]["Authorization"].startswith("Bearer ")

    def test_get_linear_mcp_config_raises_exception_without_api_key(self):
        """Test get_linear_mcp_config raises LinearApiKeyException when API key is missing."""
        with patch("chimera.services.linear.LINEAR", {"api_key": None}):
            with pytest.raises(LinearApiKeyException):
                get_linear_mcp_config()

    def test_get_linear_mcp_config_raises_exception_with_empty_api_key(self):
        """Test get_linear_mcp_config raises LinearApiKeyException when API key is empty."""
        with patch("chimera.services.linear.LINEAR", {"api_key": ""}):
            with pytest.raises(LinearApiKeyException):
                get_linear_mcp_config()

    def test_get_linear_mcp_config_config_structure(self, mock_linear_api_key):
        """Test that the returned config has the expected structure."""
        with patch("chimera.services.linear.LINEAR", {"api_key": mock_linear_api_key}):
            config = get_linear_mcp_config()

        assert isinstance(config, dict)
        assert "transport" in config
        assert "url" in config
        assert "headers" in config
        assert isinstance(config["headers"], dict)

    def test_linear_api_key_exception_is_chimera_exception(self):
        """Test that LinearApiKeyException is a ChimeraException."""
        from chimera.library.exceptions import ChimeraException

        with pytest.raises(ChimeraException):
            with patch("chimera.services.linear.LINEAR", {"api_key": None}):
                get_linear_mcp_config()
