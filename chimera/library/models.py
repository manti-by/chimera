from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID

from langchain_core.messages import BaseMessage
from slugify import slugify


@dataclass
class WorkflowState:
    messages: list[BaseMessage] = field(default_factory=list)
    llm_calls: int = 0
    project_name: str = ""
    linear_task_id: str | None = None
    branch_name: str | None = None
    worktree_path: Path | None = None
    implementation_plan: str | None = None
    build_attempts: int = 0
    review_attempts: int = 0
    needs_rebuild: bool = True
    needs_relint: bool = True
    lint_errors: str | None = None
    test_errors: str | None = None
    pr_url: str | None = None
    completed_steps: list[str] = field(default_factory=list)

    def update(self, updates: dict[str, Any]) -> "WorkflowState":
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self


@dataclass
class LinearTask:
    id: str
    identifier: str
    title: str
    description: str
    priority: str
    created_at: datetime
    state: str | None = None
    project_name: str | None = None
    project_id: str | None = None
    user_id: str | None = None
    comments: list[str] = field(default_factory=list)

    @property
    def full_title(self) -> str:
        return f"{self.identifier.strip()}: {self.title.strip()}"

    @property
    def slug(self) -> str:
        return slugify(self.full_title)

    @property
    def text(self) -> str:
        result = f"{self.title.strip()}\n({self.description.strip()})"
        if self.comments:
            result += f"\n\nComments:\n{'\n'.join(self.comments)}"
        return result


class ProjectStatus(Enum):
    CREATED = "created"
    SET_UP = "set_up"
    ERROR = "error"
    TEAR_DOWN = "tear_down"
    DONE = "done"


@dataclass
class Project:
    id: str
    name: str
    linear_id: str | None
    repository_url: str
    repository_name: str
    repository_owner: str
    local_path: Path
    created_at: datetime
    updated_at: datetime
    status: str = "created"


class SessionStatus(Enum):
    CREATED = "created"
    SET_UP = "set_up"
    PLANNING = "planning"
    AWAITING_INPUT = "awaiting_input"
    BUILDING = "building"
    IN_REVIEW = "in_review"
    LINTING = "linting"
    TESTING = "testing"
    TEAR_DOWN = "tear_down"
    DONE = "done"


@dataclass
class Session:
    id: UUID
    project: Project
    linear_task: LinearTask
    created_at: datetime
    updated_at: datetime
    auto_mode: bool
    worktree_path: Path
    status: str = SessionStatus.CREATED.value
    build_plan: str | None = None
    opencode_session_id: str | None = None
    posted_to_linear: bool = False
