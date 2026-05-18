from pathlib import Path


class TestSettings:
    """Test cases for settings configuration."""

    def test_home_path_points_to_home(self):
        """Test that HOME_PATH points to the user's home directory."""
        from chimera import settings

        assert settings.HOME_PATH == Path.home()

    def test_base_path_is_project_root(self):
        """Test that BASE_PATH points to the project root."""
        from chimera import settings

        assert settings.BASE_PATH.exists()
        assert (settings.BASE_PATH / "chimera").exists()

    def test_db_url_is_configured(self):
        """Test that DB_URL is a valid PostgreSQL connection string."""
        from chimera import settings

        assert settings.DB_URL.startswith("postgresql+asyncpg://")
        assert "chimera" in settings.DB_URL

    def test_worktree_path_default(self):
        """Test that WORKTREE_PATH has a default value."""
        from chimera import settings

        assert ".chimera" in str(settings.WORKTREE_PATH)
        assert "worktrees" in str(settings.WORKTREE_PATH)

    def test_max_attempts_have_defaults(self):
        """Test that MAX_BUILD_ATTEMPTS and MAX_REVIEW_ATTEMPTS have default values."""
        from chimera import settings

        assert settings.MAX_BUILD_ATTEMPTS >= 0
        assert settings.MAX_REVIEW_ATTEMPTS >= 0
        assert isinstance(settings.MAX_BUILD_ATTEMPTS, int)
        assert isinstance(settings.MAX_REVIEW_ATTEMPTS, int)

    def test_log_path_default(self):
        """Test that LOG_PATH has a default value."""
        from chimera import settings

        assert "chimera" in str(settings.LOG_PATH)
        assert settings.LOG_PATH.suffix == ".log"

    def test_logging_config_structure(self):
        """Test that LOGGING config has required structure."""
        from chimera import settings

        assert "version" in settings.LOGGING
        assert "formatters" in settings.LOGGING
        assert "handlers" in settings.LOGGING
        assert "loggers" in settings.LOGGING
        assert "standard" in settings.LOGGING["formatters"]
        assert "console" in settings.LOGGING["handlers"]
        assert "file" in settings.LOGGING["handlers"]

    def test_linear_config_structure(self):
        """Test that LINEAR config has correct structure."""
        from chimera import settings

        assert "api_key" in settings.LINEAR

    def test_opencode_config_structure(self):
        """Test that OPENCODE config has correct structure."""
        from chimera import settings

        assert "path" in settings.OPENCODE
        assert "plan_model" in settings.OPENCODE
        assert "build_model" in settings.OPENCODE
        assert "review_models" in settings.OPENCODE
        assert isinstance(settings.OPENCODE["review_models"], list)

    def test_git_config_structure(self):
        """Test that GIT config has correct structure."""
        from chimera import settings

        assert "path" in settings.GIT
        assert "worktree_path" in settings.GIT
        assert isinstance(settings.GIT["path"], Path)
        assert isinstance(settings.GIT["worktree_path"], Path)

    def test_groq_config_structure(self):
        """Test that GROQ config has correct structure."""
        from chimera import settings

        assert "api_key" in settings.GROQ
        assert "model" in settings.GROQ

    def test_github_config_structure(self):
        """Test that GITHUB config has correct structure."""
        from chimera import settings

        assert "path" in settings.GITHUB
        assert isinstance(settings.GITHUB["path"], Path)

    def test_uv_config_structure(self):
        """Test that UV config has correct structure."""
        from chimera import settings

        assert "path" in settings.UV
        assert isinstance(settings.UV["path"], Path)

    def test_coderabbit_config_structure(self):
        """Test that CODERABBIT config has correct structure."""
        from chimera import settings

        assert "path" in settings.CODERABBIT
        assert "config_path" in settings.CODERABBIT

    def test_projects_path_default(self):
        """Test that PROJECTS_PATH has a default value."""
        from chimera import settings

        assert "projects" in str(settings.PROJECTS_PATH)

    def test_settings_can_be_overridden_via_env(self, monkeypatch):
        """Test that settings can be overridden via environment variables."""
        monkeypatch.setenv("MAX_BUILD_ATTEMPTS", "50")
        monkeypatch.setenv("MAX_REVIEW_ATTEMPTS", "25")

        import importlib

        import chimera.settings as settings_module

        importlib.reload(settings_module)

        try:
            assert settings_module.MAX_BUILD_ATTEMPTS == 50
            assert settings_module.MAX_REVIEW_ATTEMPTS == 25
        finally:
            # Restore original module state
            monkeypatch.delenv("MAX_BUILD_ATTEMPTS", raising=False)
            monkeypatch.delenv("MAX_REVIEW_ATTEMPTS", raising=False)
            importlib.reload(settings_module)

    def test_opencode_path_default(self):
        """Test that OPENCODE path defaults to home directory."""
        from chimera import settings

        assert ".opencode" in str(settings.OPENCODE["path"])

    def test_git_path_default(self):
        """Test that GIT path defaults to /usr/bin/git."""
        from chimera import settings

        assert "git" in str(settings.GIT["path"]).lower()

    def test_groq_model_default(self):
        """Test that GROQ model has a default value."""
        from chimera import settings

        assert settings.GROQ["model"] is not None
        assert len(settings.GROQ["model"]) > 0
