from pathlib import Path

from pydantic import BaseModel


class Context(BaseModel):
    project_name: str
    project_path: Path

    def __str__(self) -> str:
        return f"Context(project_name='{self.project_name}', project_path='{self.project_path}')"
