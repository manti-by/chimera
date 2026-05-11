import json
import shlex
from pathlib import Path

from chimera.services.subprocess import run_command
from chimera.settings import OPENCODE


async def run_opencode_agent(
    target_path: Path,
    task: str,
    model: str,
    agent: str,
    session_id: str | None = None,
    task_title: str | None = None,
    disable_stdio: bool = False,
) -> tuple[int, str, str]:
    command = [str(OPENCODE["path"]), "run", "--model", model, "--agent", agent]

    if session_id is not None:
        command.extend(["--session", session_id])
    if task_title is not None:
        command.extend(["--title", task_title])

    command.append(shlex.quote(task)[:4095])
    return await run_command(command=command, target_path=target_path, disable_stdio=disable_stdio)


async def get_opencode_sessions(target_path: Path) -> list[dict[str, str]]:
    command = [str(OPENCODE["path"]), "session", "list", "--format", "json"]
    _, result, _ = await run_command(command=command, target_path=target_path, disable_stdio=True)
    return json.loads(result)


async def get_opencode_session_id(target_path: Path, task_title: str) -> str | None:
    sessions = await get_opencode_sessions(target_path=target_path)
    for session in sorted(sessions, key=lambda x: x["updated"], reverse=True):
        if session["title"] == task_title and session["directory"] == str(target_path):
            return session["id"]
    return None
