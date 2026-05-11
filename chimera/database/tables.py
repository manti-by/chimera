from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    MetaData,
    String,
    Table,
    Text,
)


metadata = MetaData()

projects = Table(
    "projects",
    metadata,
    Column("id", String(), primary_key=True),
    Column("name", String(), nullable=False),
    Column("linear_id", String(), nullable=True),
    Column("repository_url", String(), nullable=False),
    Column("repository_name", String(), nullable=False),
    Column("repository_owner", String(), nullable=False),
    Column("local_path", String(), nullable=False),
    Column("status", String(), server_default="created", nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)


sessions = Table(
    "sessions",
    metadata,
    Column("id", String(), primary_key=True),
    Column("project_id", String(), index=True, nullable=False),
    Column("linear_task_id", String(), index=True, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    Column("auto_mode", Boolean(), nullable=False, server_default="true"),
    Column("worktree_path", String(), nullable=True),
    Column("status", String(), nullable=False, server_default="created"),
    Column("opencode_session_id", String(), index=True, nullable=True),
    Column("build_plan", Text(), nullable=True, server_default=None),
    Column("posted_to_linear", Boolean(), nullable=False, server_default="false"),
)
