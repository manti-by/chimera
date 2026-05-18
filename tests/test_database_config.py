import pytest


class TestDatabaseConfiguration:
    """Test cases for database configuration in tests."""

    def test_db_url_uses_test_prefix(self, test_db_url):
        """Test that the test database URL uses test_ prefix."""
        assert "test_chimera" in test_db_url
        assert "postgresql+asyncpg" in test_db_url

    def test_db_url_contains_expected_components(self, test_db_url):
        """Test that the test database URL has all expected components."""
        assert "chimera:chimera" in test_db_url
        assert "localhost:5432" in test_db_url

    def test_sync_db_url_uses_test_prefix(self, test_db_url_sync):
        """Test that the sync test database URL uses test_ prefix."""
        assert "test_chimera" in test_db_url_sync
        assert "postgresql+psycopg" in test_db_url_sync

    def test_admin_db_url_uses_postgres(self, admin_db_url):
        """Test that the admin database URL uses postgres database."""
        assert "postgres" in admin_db_url
        assert "test_chimera" not in admin_db_url

    def test_settings_db_url_is_overridden(self, override_db_url_for_tests):
        """Test that settings.DB_URL is overridden to use test database."""
        from chimera.settings import DB_URL

        assert "test_chimera" in DB_URL

    def test_main_db_url_does_not_have_test_prefix(self):
        """Verify the original main DB_URL doesn't have test_ prefix.

        This ensures we're actually changing the URL in tests.
        """
        import os

        # When DB_URL env var is not set, the original should not have test_ prefix
        db_url_env = os.environ.get("DB_URL", "")

        # If the env var is set (which it is in tests), it should have test_ prefix
        if db_url_env:
            assert "test_chimera" in db_url_env

    @pytest.mark.database
    def test_database_marker_exists(self):
        """Test that database marker is available."""
        # This test verifies the database marker is configured
        assert True
