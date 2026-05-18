import pytest

from chimera.library.exceptions import ChimeraException, LinearApiKeyException


class TestChimeraException:
    """Test cases for ChimeraException."""

    def test_chimera_exception_is_base_exception(self):
        """Test that ChimeraException inherits from BaseException."""
        assert issubclass(ChimeraException, BaseException)

    def test_chimera_exception_can_be_raised(self):
        """Test that ChimeraException can be raised and caught."""
        with pytest.raises(ChimeraException):
            raise ChimeraException("Test error")

    def test_chimera_exception_message(self):
        """Test that ChimeraException preserves error message."""
        message = "Custom error message"

        with pytest.raises(ChimeraException) as exc_info:
            raise ChimeraException(message)

        assert str(exc_info.value) == message

    def test_chimera_exception_is_catchable_as_baseexception(self):
        """Test that ChimeraException can be caught as BaseException."""
        try:
            raise ChimeraException("Test")
        except BaseException as e:  # noqa
            assert isinstance(e, ChimeraException)


class TestLinearApiKeyException:
    """Test cases for LinearApiKeyException."""

    def test_linear_api_key_exception_inheritance(self):
        """Test that LinearApiKeyException inherits from ChimeraException."""
        assert issubclass(LinearApiKeyException, ChimeraException)

    def test_linear_api_key_exception_can_be_raised(self):
        """Test that LinearApiKeyException can be raised and caught."""
        with pytest.raises(LinearApiKeyException):
            raise LinearApiKeyException("API key missing")

    def test_linear_api_key_exception_message(self):
        """Test that LinearApiKeyException preserves error message."""
        message = "Linear API key is not configured"

        with pytest.raises(LinearApiKeyException) as exc_info:
            raise LinearApiKeyException(message)

        assert str(exc_info.value) == message

    def test_linear_api_key_exception_is_catchable_as_chimera(self):
        """Test that LinearApiKeyException can be caught as ChimeraException."""
        try:
            raise LinearApiKeyException("Test")
        except ChimeraException as e:
            assert isinstance(e, LinearApiKeyException)

    def test_linear_api_key_exception_is_catchable_as_baseexception(self):
        """Test that LinearApiKeyException can be caught as BaseException."""
        try:
            raise LinearApiKeyException("Test")
        except BaseException as e:  # noqa
            assert isinstance(e, LinearApiKeyException)
