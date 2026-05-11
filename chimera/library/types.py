from pathlib import Path
from typing import TypedDict


class LinearConfig(TypedDict):
    api_key: str | None


class OpenCodeConfig(TypedDict):
    path: Path
    plan_model: str
    build_model: str
    review_models: list[str]


class GitConfig(TypedDict):
    path: Path
    worktree_path: Path


class GroqConfig(TypedDict):
    api_key: str | None
    model: str
