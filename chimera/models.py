from pathlib import Path

from pydantic import BaseModel
from slugify import slugify


class Context(BaseModel):
    project_name: str
    project_path: Path
    worktree_path: Path | None = None


class LinearTask(BaseModel):
    id: str
    identifier: str
    title: str
    description: str
    priority: str
    created_at: str
    branch_name: str
    comments: list[str] = []

    @property
    def text(self) -> str:
        if self.comments:
            return f"{self.title}\n({self.description})\n\nComments:\n{'\n'.join(self.comments)}"
        return f"{self.title}\n({self.description})"

    @property
    def slug(self) -> str:
        return slugify(f"{self.identifier}-{self.title}")
