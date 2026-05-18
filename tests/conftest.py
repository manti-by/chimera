"""Test configuration and fixtures for Chimera."""

import asyncio
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import pytest_asyncio


# Test database configuration - uses test_ prefix
TEST_DB_NAME = "test_chimera"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_path(tmp_path):
    """Create a temporary path for testing."""
    return tmp_path


@pytest.fixture
def mock_branch_name():
    """Generate a mock branch name."""
    return f"feature/test-branch-{uuid4().hex[:8]}"


@pytest.fixture
def mock_session_id():
    """Generate a mock session ID."""
    return f"session-{uuid4().hex[:8]}"


@pytest.fixture
def mock_task_title():
    """Generate a mock task title."""
    return f"Test Task {uuid4().hex[:8]}"


@pytest.fixture
def mock_linear_api_key():
    """Generate a mock Linear API key."""
    return f"lin_api_{uuid4().hex[:24]}"


@pytest.fixture
def mock_command_output():
    """Mock successful command output."""
    return (0, "stdout output", "")


@pytest.fixture
def mock_command_error():
    """Mock failed command output."""
    return (1, "", "error message")


@pytest.fixture
def mock_process():
    """Create a mock subprocess process."""
    mock_stdout = AsyncMock()
    mock_stdout.readline = AsyncMock(side_effect=[b"line 1\n", b"line 2\n", b""])

    mock_stderr = AsyncMock()
    mock_stderr.readline = AsyncMock(side_effect=[b"error 1\n", b""])

    mock_proc = MagicMock()
    mock_proc.stdout = mock_stdout
    mock_proc.stderr = mock_stderr
    mock_proc.kill = MagicMock()
    mock_proc.wait = AsyncMock(return_value=0)

    return mock_proc


@pytest.fixture
def mock_process_failure():
    """Create a mock subprocess process that fails."""
    mock_stdout = AsyncMock()
    mock_stdout.readline = AsyncMock(side_effect=[b""])

    mock_stderr = AsyncMock()
    mock_stderr.readline = AsyncMock(side_effect=[b"error message\n", b""])

    mock_proc = MagicMock()
    mock_proc.stdout = mock_stdout
    mock_proc.stderr = mock_stderr
    mock_proc.kill = MagicMock()
    mock_proc.wait = AsyncMock(return_value=1)

    return mock_proc


@pytest.fixture
def linear_task_data():
    """Create mock Linear task data."""
    return {
        "id": f"issue-{uuid4().hex[:8]}",
        "identifier": f"CHI-{uuid4().hex[:4].upper()}",
        "title": "Test Linear Task",
        "description": "This is a test task description",
        "priority": "high",
        "created_at": datetime.now(),
        "state": "todo",
        "project_name": "chimera",
        "project_id": f"project-{uuid4().hex[:8]}",
        "user_id": f"user-{uuid4().hex[:8]}",
        "comments": [],
    }


@pytest.fixture
def linear_task_data_with_comments(linear_task_data):
    """Create mock Linear task data with comments."""
    linear_task_data["comments"] = [
        "First comment about the task",
        "Second comment with questions",
    ]
    return linear_task_data


@pytest.fixture
def project_data():
    """Create mock Project data."""
    return {
        "id": str(uuid4()),
        "name": "chimera",
        "linear_id": f"linear-{uuid4().hex[:8]}",
        "repository_url": "https://github.com/test/chimera",
        "repository_name": "chimera",
        "repository_owner": "test",
        "local_path": Path("/home/test/projects/chimera"),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "status": "created",
    }


@pytest.fixture
def session_data(project_data, linear_task_data):
    """Create mock Session data."""
    from chimera.library.models import LinearTask, Project

    project = Project(**project_data)
    linear_task = LinearTask(**linear_task_data)

    return {
        "id": uuid4(),
        "project": project,
        "linear_task": linear_task,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "auto_mode": False,
        "worktree_path": Path("/tmp/worktree/test"),  # noqa
        "status": "created",
        "build_plan": None,
        "opencode_session_id": None,
        "posted_to_linear": False,
    }


@pytest.fixture
def workflow_state_data():
    """Create mock WorkflowState data."""
    return {
        "messages": [],
        "llm_calls": 0,
        "project_name": "chimera",
        "linear_task_id": f"task-{uuid4().hex[:8]}",
        "branch_name": "feature/test-branch",
        "worktree_path": Path("/tmp/worktree/test"),  # noqa
        "implementation_plan": "1. Step one\n2. Step two",
        "build_attempts": 0,
        "review_attempts": 0,
        "needs_rebuild": True,
        "needs_relint": True,
        "lint_errors": None,
        "test_errors": None,
        "pr_url": None,
        "completed_steps": [],
    }


@pytest_asyncio.fixture
async def mock_run_command():
    """Mock the run_command function."""
    with patch("chimera.services.subprocess.run_command", new_callable=AsyncMock) as mock:
        mock.return_value = (0, "success", "")
        yield mock


@pytest.fixture
def mock_settings_env(monkeypatch):
    """Set up mock environment variables for settings."""
    monkeypatch.setenv("LINEAR_API_KEY", "test-api-key")
    monkeypatch.setenv("GROQ_API_KEY", "test-groq-key")
    monkeypatch.setenv("MAX_BUILD_ATTEMPTS", "10")
    monkeypatch.setenv("MAX_REVIEW_ATTEMPTS", "5")


@pytest.fixture
def opencode_sessions_data():
    """Create mock opencode session data."""
    return [
        {
            "id": f"session-{uuid4().hex[:8]}",
            "title": "Test Session 1",
            "directory": "/home/test/project",
            "updated": "2024-01-01T00:00:00Z",
        },
        {
            "id": f"session-{uuid4().hex[:8]}",
            "title": "Test Session 2",
            "directory": "/home/test/project",
            "updated": "2024-01-02T00:00:00Z",
        },
    ]


@pytest.fixture(scope="session")
def test_db_url():
    """Provide the test database URL with test_ prefix.

    Uses the same connection as the main app but with 'test_chimera' database.
    """
    return "postgresql+asyncpg://chimera:chimera@localhost:5432/test_chimera"


@pytest.fixture(scope="session")
def test_db_url_sync():
    """Provide the synchronous test database URL with test_ prefix."""
    return "postgresql+psycopg://chimera:chimera@localhost:5432/test_chimera"


@pytest.fixture(scope="session")
def admin_db_url():
    """Provide the admin database URL for creating/dropping test database."""
    return "postgresql+asyncpg://chimera:chimera@localhost:5432/postgres"


@pytest.fixture(autouse=True)
def override_db_url_for_tests(monkeypatch, test_db_url):
    """Override the DB_URL in settings to use the test database.

    This fixture runs automatically for all tests.
    """
    monkeypatch.setenv("DB_URL", test_db_url)

    # Reload settings module to pick up the new env var
    import importlib  # noqa

    import chimera.database.connection as connection_module
    import chimera.settings as settings_module

    # Override with test database URL
    monkeypatch.setattr(settings_module, "DB_URL", test_db_url)

    yield

    # Restore original (monkeypatch will handle this, but we clear cache)
    connection_module._engine_cache.clear()
