import os
from pathlib import Path

from chimera.library.types import (
    GitConfig,
    GroqConfig,
    LinearConfig,
    OpenCodeConfig,
)


HOME_PATH = Path.home()

BASE_PATH = Path(__file__).resolve().parent.parent

DB_URL = "postgresql+asyncpg://chimera:chimera@localhost:5432/chimera"  # noqa
DB_USER = os.environ.get("DB_USER", "chimera")

WORKTREE_PATH = HOME_PATH / ".chimera" / "worktrees"

MAX_BUILD_ATTEMPTS = int(os.environ.get("MAX_BUILD_ATTEMPTS", 30))
MAX_REVIEW_ATTEMPTS = int(os.environ.get("MAX_REVIEW_ATTEMPTS", 30))

LOG_PATH = Path(os.environ.get("LOG_PATH", "/var/log/chimera/workflow.log")).resolve()

LOGGING: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)-6s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": "INFO", "propagate": True},
    },
}

LINEAR: LinearConfig = {
    "api_key": os.environ.get("LINEAR_API_KEY"),
}

OPENCODE: OpenCodeConfig = {
    "path": Path(os.environ.get("OPENCODE_PATH", HOME_PATH / ".opencode/bin/opencode")).resolve(),
    "plan_model": os.environ.get("OPENCODE_PLAN_MODEL", "opencode/minimax-m2.5-free"),
    "build_model": os.environ.get("OPENCODE_BUILD_MODEL", "opencode/minimax-m2.5-free"),
    "review_models": os.environ.get(
        "OPENCODE_REVIEW_MODELS",
        "opencode/big-pickle,opencode/minimax-m2.5-free",
    ).split(","),
}

GIT: GitConfig = {
    "path": Path(os.environ.get("GIT_PATH", "/usr/bin/git")).resolve(),
    "worktree_path": Path(os.environ.get("GIT_WORKTREE_PATH", HOME_PATH / ".chimera/worktrees/")).resolve(),
}

GROQ: GroqConfig = {
    "api_key": os.environ.get("GROQ_API_KEY"),
    "model": os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant"),
}

GITHUB: dict[str, Path] = {
    "path": Path(os.environ.get("GH_PATH", "/usr/bin/gh")).resolve(),
}

UV: dict[str, Path] = {
    "path": Path(os.environ.get("UV_PATH", HOME_PATH / ".local/bin/uv")).resolve(),
}

CODERABBIT: dict[str, Path | str] = {
    "path": Path(os.environ.get("CODERABBIT_PATH", HOME_PATH / ".local/bin/coderabbit")),
    "config_path": Path(os.environ.get("CODERABBIT_CONFIG_PATH", HOME_PATH / ".coderabbit.yaml")),
}

PROJECTS_PATH = Path(os.environ.get("PROJECTS_PATH", HOME_PATH / "projects"))
