from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import insert, select

from chimera.database.connection import get_connection
from chimera.database.tables import projects, sessions
from chimera.library.models import Project, Session


async def create_session(
    project_id: str,
    linear_task_id: str,
    auto_mode: bool = False,
    worktree_path: str | None = None,
    status: str = "created",
    opencode_session_id: str | None = None,
    build_plan: str | None = None,
    posted_to_linear: bool = False,
) -> Session:
    now = datetime.now(UTC)
    session_data = {
        "id": str(uuid4()),
        "project_id": project_id,
        "linear_task_id": linear_task_id,
        "created_at": now,
        "updated_at": now,
        "auto_mode": auto_mode,
        "worktree_path": worktree_path,
        "status": status,
        "opencode_session_id": opencode_session_id,
        "build_plan": build_plan,
        "posted_to_linear": posted_to_linear,
    }
    async with get_connection() as connection:
        await connection.execute(insert(sessions).values(**session_data))
        await connection.commit()
    return Session(**session_data)  # ty: ignore[invalid-argument-type]


async def get_session(session_id: str) -> Session | None:
    async with get_connection() as connection:
        result = await connection.execute(select(sessions).where(sessions.c.id == session_id))
        row = result.fetchone()
    return Session(**row._mapping) if row else None


async def mark_session_posted(session_id: str) -> None:
    now = datetime.now(UTC)
    async with get_connection() as connection:
        await connection.execute(
            sessions.update().where(sessions.c.id == session_id).values(posted_to_linear=True, updated_at=now)
        )
        await connection.commit()


async def get_sessions(status: str | None = None) -> list[Session]:
    async with get_connection() as connection:
        if status:
            result = await connection.execute(
                select(sessions).where(sessions.c.status == status).order_by(sessions.c.created_at.desc())
            )
        else:
            result = await connection.execute(select(sessions).order_by(sessions.c.created_at.desc()))
        rows = result.fetchall()
    return [Session(**row._mapping) for row in rows]


async def update_session_status(session_id: str, status: str) -> None:
    async with get_connection() as connection:
        await connection.execute(
            sessions.update().where(sessions.c.id == session_id).values(status=status, updated_at=datetime.now(UTC))
        )
        await connection.commit()


async def get_pending_session_task_ids() -> set[str]:
    async with get_connection() as connection:
        result = await connection.execute(
            select(sessions.c.task_id).where(
                sessions.c.status.not_in(["processed", "failed"]),
                sessions.c.session_id == "",
            )
        )
        rows = result.fetchall()
    return {row.task_id for row in rows}


async def create_project(
    name: str,
    repository_url: str,
    repository_name: str,
    repository_owner: str,
    linear_id: str | None = None,
    local_path: str | None = None,
    status: str = "created",
) -> Project:
    now = datetime.now(UTC)
    project_data = {
        "id": str(uuid4()),
        "name": name,
        "linear_id": linear_id,
        "repository_url": repository_url,
        "repository_name": repository_name,
        "repository_owner": repository_owner,
        "local_path": local_path,
        "status": status,
        "created_at": now,
        "updated_at": now,
    }
    async with get_connection() as connection:
        await connection.execute(insert(projects).values(**project_data))
        await connection.commit()
    return Project(**project_data)  # ty: ignore[invalid-argument-type]


async def get_project_by_id(project_id: str, user_id: str) -> Project | None:
    async with get_connection() as connection:
        result = await connection.execute(select(projects).where(projects.c.id == project_id))
        row = result.fetchone()
    return Project(**row._mapping) if row else None


async def update_project(
    project_id: str,
    linear_id: str | None = None,
    name: str | None = None,
    repository_url: str | None = None,
    repository_name: str | None = None,
    repository_owner: str | None = None,
    local_path: str | None = None,
    status: str | None = None,
) -> Project | None:
    update_values: dict[str, str | datetime] = {"updated_at": datetime.now(UTC)}
    if linear_id is not None:
        update_values["linear_id"] = linear_id
    if name is not None:
        update_values["name"] = name
    if repository_url is not None:
        update_values["repository_url"] = repository_url
    if repository_name is not None:
        update_values["repository_name"] = repository_name
    if repository_owner is not None:
        update_values["repository_owner"] = repository_owner
    if local_path is not None:
        update_values["local_path"] = local_path
    if status is not None:
        update_values["status"] = status

    async with get_connection() as connection:
        await connection.execute(projects.update().where(projects.c.id == project_id).values(**update_values))
        await connection.commit()

        result = await connection.execute(select(projects).where(projects.c.id == project_id))
        row = result.fetchone()
    return Project(**row._mapping) if row else None


async def delete_project(project_id: str) -> None:
    async with get_connection() as connection:
        await connection.execute(projects.delete().where(projects.c.id == project_id))
        await connection.commit()
