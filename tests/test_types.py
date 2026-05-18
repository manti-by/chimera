from pathlib import Path

from chimera.library.types import GitConfig, GroqConfig, LinearConfig, OpenCodeConfig


class TestLinearConfig:
    """Test cases for LinearConfig TypedDict."""

    def test_linear_config_structure(self):
        """Test that LinearConfig has the expected structure."""
        config: LinearConfig = {"api_key": "test-key"}

        assert "api_key" in config
        assert config["api_key"] == "test-key"

    def test_linear_config_optional_api_key(self):
        """Test that LinearConfig api_key can be None."""
        config: LinearConfig = {"api_key": None}

        assert config["api_key"] is None


class TestOpenCodeConfig:
    """Test cases for OpenCodeConfig TypedDict."""

    def test_opencode_config_structure(self):
        """Test that OpenCodeConfig has the expected structure."""
        config: OpenCodeConfig = {
            "path": Path("/usr/bin/opencode"),
            "plan_model": "model-1",
            "build_model": "model-2",
            "review_models": ["model-3", "model-4"],
        }

        assert "path" in config
        assert "plan_model" in config
        assert "build_model" in config
        assert "review_models" in config
        assert isinstance(config["path"], Path)
        assert isinstance(config["review_models"], list)

    def test_opencode_config_review_models_is_list(self):
        """Test that review_models is a list of strings."""
        config: OpenCodeConfig = {
            "path": Path("/usr/bin/opencode"),
            "plan_model": "plan-model",
            "build_model": "build-model",
            "review_models": ["review-1", "review-2"],
        }

        assert len(config["review_models"]) == 2
        assert all(isinstance(m, str) for m in config["review_models"])


class TestGitConfig:
    """Test cases for GitConfig TypedDict."""

    def test_git_config_structure(self):
        """Test that GitConfig has the expected structure."""
        config: GitConfig = {
            "path": Path("/usr/bin/git"),
            "worktree_path": Path("/tmp/worktrees"),  # noqa
        }

        assert "path" in config
        assert "worktree_path" in config
        assert isinstance(config["path"], Path)
        assert isinstance(config["worktree_path"], Path)

    def test_git_config_paths_exist(self, tmp_path):
        """Test that GitConfig paths can be created."""
        git_path = tmp_path / "git"
        worktree_path = tmp_path / "worktrees"

        config: GitConfig = {
            "path": git_path,
            "worktree_path": worktree_path,
        }

        assert config["path"] == git_path
        assert config["worktree_path"] == worktree_path


class TestGroqConfig:
    """Test cases for GroqConfig TypedDict."""

    def test_groq_config_structure(self):
        """Test that GroqConfig has the expected structure."""
        config: GroqConfig = {
            "api_key": "test-api-key",
            "model": "llama-3.3-70b",
        }

        assert "api_key" in config
        assert "model" in config
        assert config["api_key"] == "test-api-key"
        assert config["model"] == "llama-3.3-70b"

    def test_groq_config_optional_api_key(self):
        """Test that GroqConfig api_key can be None."""
        config: GroqConfig = {
            "api_key": None,
            "model": "default-model",
        }

        assert config["api_key"] is None
        assert config["model"] == "default-model"
