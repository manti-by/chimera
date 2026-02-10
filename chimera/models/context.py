from pathlib import Path

from pydantic.dataclasses import dataclass


@dataclass
class Context:
    project_name: str
    project_path: Path
