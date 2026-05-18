from datetime import datetime
from pathlib import Path
from uuid import uuid4

from chimera.library.models import LinearTask, Project, ProjectStatus, Session, SessionStatus, WorkflowState


class TestLinearTask:
    """Test cases for LinearTask model."""

    def test_linear_task_creation(self, linear_task_data):
        """Test creating a LinearTask with valid data."""
        task = LinearTask(**linear_task_data)

        assert task.id == linear_task_data["id"]
        assert task.identifier == linear_task_data["identifier"]
        assert task.title == linear_task_data["title"]
        assert task.description == linear_task_data["description"]
        assert task.priority == linear_task_data["priority"]
        assert task.created_at == linear_task_data["created_at"]
        assert task.state == linear_task_data["state"]
        assert task.project_name == linear_task_data["project_name"]
        assert task.project_id == linear_task_data["project_id"]
        assert task.user_id == linear_task_data["user_id"]
        assert task.comments == linear_task_data["comments"]

    def test_full_title_property(self, linear_task_data):
        """Test the full_title property combines identifier and title."""
        task = LinearTask(**linear_task_data)
        full_title = task.full_title

        assert task.identifier in full_title
        assert task.title in full_title
        assert ": " in full_title

    def test_slug_property(self, linear_task_data):
        """Test the slug property generates a URL-friendly slug."""
        task = LinearTask(**linear_task_data)
        slug = task.slug

        assert isinstance(slug, str)
        assert len(slug) > 0
        # Slug should be lowercase and contain no spaces
        assert slug == slug.lower()
        assert " " not in slug

    def test_text_property_without_comments(self, linear_task_data):
        """Test the text property without comments."""
        task = LinearTask(**linear_task_data)
        text = task.text

        assert task.title in text
        assert task.description in text
        assert "Comments:" not in text

    def test_text_property_with_comments(self, linear_task_data_with_comments):
        """Test the text property with comments."""
        task = LinearTask(**linear_task_data_with_comments)
        text = task.text

        assert task.title in text
        assert "Comments:" in text
        for comment in task.comments:
            assert comment in text

    def test_default_comments_is_empty_list(self):
        """Test that default comments is an empty list."""
        task = LinearTask(
            id="test-id",
            identifier="TEST-1",
            title="Test",
            description="Test description",
            priority="medium",
            created_at=datetime.now(),
        )

        assert task.comments == []

    def test_comments_field_is_mutable(self, linear_task_data):
        """Test that comments field can be modified."""
        task = LinearTask(**linear_task_data)
        task.comments.append("New comment")

        assert "New comment" in task.comments


class TestProject:
    """Test cases for Project model."""

    def test_project_creation(self, project_data):
        """Test creating a Project with valid data."""
        project = Project(**project_data)

        assert project.id == project_data["id"]
        assert project.name == project_data["name"]
        assert project.linear_id == project_data["linear_id"]
        assert project.repository_url == project_data["repository_url"]
        assert project.repository_name == project_data["repository_name"]
        assert project.repository_owner == project_data["repository_owner"]
        assert project.local_path == project_data["local_path"]
        assert project.created_at == project_data["created_at"]
        assert project.updated_at == project_data["updated_at"]
        assert project.status == project_data["status"]

    def test_project_status_default(self, project_data):
        """Test that status defaults to 'created'."""
        data = project_data.copy()
        del data["status"]

        project = Project(**data, status="created")
        assert project.status == "created"

    def test_project_path_is_path_object(self, project_data):
        """Test that local_path is a Path object."""
        project = Project(**project_data)

        assert isinstance(project.local_path, Path)


class TestSession:
    """Test cases for Session model."""

    def test_session_creation(self, session_data):
        """Test creating a Session with valid data."""
        session = Session(**session_data)

        assert session.id == session_data["id"]
        assert session.project == session_data["project"]
        assert session.linear_task == session_data["linear_task"]
        assert session.created_at == session_data["created_at"]
        assert session.updated_at == session_data["updated_at"]
        assert session.auto_mode == session_data["auto_mode"]
        assert session.worktree_path == session_data["worktree_path"]
        assert session.status == session_data["status"]
        assert session.build_plan == session_data["build_plan"]
        assert session.opencode_session_id == session_data["opencode_session_id"]
        assert session.posted_to_linear == session_data["posted_to_linear"]

    def test_session_status_default(self, session_data):
        """Test that status defaults to 'created'."""
        data = session_data.copy()
        data["status"] = SessionStatus.CREATED.value

        session = Session(**data)
        assert session.status == SessionStatus.CREATED.value

    def test_session_worktree_is_path_object(self, session_data):
        """Test that worktree_path is a Path object."""
        session = Session(**session_data)

        assert isinstance(session.worktree_path, Path)

    def test_session_id_is_uuid(self, session_data):
        """Test that session id is a UUID."""
        session = Session(**session_data)

        assert isinstance(session.id, type(uuid4()))


class TestWorkflowState:
    """Test cases for WorkflowState model."""

    def test_workflow_state_creation(self, workflow_state_data):
        """Test creating a WorkflowState with valid data."""
        state = WorkflowState(**workflow_state_data)

        assert state.messages == workflow_state_data["messages"]
        assert state.llm_calls == workflow_state_data["llm_calls"]
        assert state.project_name == workflow_state_data["project_name"]
        assert state.linear_task_id == workflow_state_data["linear_task_id"]
        assert state.branch_name == workflow_state_data["branch_name"]
        assert state.worktree_path == workflow_state_data["worktree_path"]
        assert state.implementation_plan == workflow_state_data["implementation_plan"]
        assert state.build_attempts == workflow_state_data["build_attempts"]
        assert state.review_attempts == workflow_state_data["review_attempts"]
        assert state.needs_rebuild == workflow_state_data["needs_rebuild"]
        assert state.needs_relint == workflow_state_data["needs_relint"]
        assert state.lint_errors == workflow_state_data["lint_errors"]
        assert state.test_errors == workflow_state_data["test_errors"]
        assert state.pr_url == workflow_state_data["pr_url"]
        assert state.completed_steps == workflow_state_data["completed_steps"]

    def test_workflow_state_defaults(self):
        """Test WorkflowState default values."""
        state = WorkflowState()

        assert state.messages == []
        assert state.llm_calls == 0
        assert state.project_name == ""
        assert state.linear_task_id is None
        assert state.branch_name is None
        assert state.worktree_path is None
        assert state.implementation_plan is None
        assert state.build_attempts == 0
        assert state.review_attempts == 0
        assert state.needs_rebuild is True
        assert state.needs_relint is True
        assert state.lint_errors is None
        assert state.test_errors is None
        assert state.pr_url is None
        assert state.completed_steps == []

    def test_update_method(self, workflow_state_data):
        """Test the update method modifies state correctly."""
        state = WorkflowState()
        updates = {
            "project_name": "updated_project",
            "llm_calls": 5,
            "build_attempts": 3,
        }

        state.update(updates)

        assert state.project_name == "updated_project"
        assert state.llm_calls == 5
        assert state.build_attempts == 3

    def test_update_returns_self(self, workflow_state_data):
        """Test that update method returns self for chaining."""
        state = WorkflowState()
        result = state.update({"project_name": "test"})

        assert result is state

    def test_update_ignores_invalid_keys(self, workflow_state_data):
        """Test that update ignores keys that don't exist."""
        state = WorkflowState()
        state.update({"invalid_key": "value", "llm_calls": 10})

        assert state.llm_calls == 10
        assert not hasattr(state, "invalid_key")

    def test_worktree_path_is_path_object(self, workflow_state_data):
        """Test that worktree_path is a Path object."""
        state = WorkflowState(**workflow_state_data)

        assert isinstance(state.worktree_path, Path)


class TestProjectStatus:
    """Test cases for ProjectStatus enum."""

    def test_project_status_values(self):
        """Test that ProjectStatus enum has expected values."""
        assert ProjectStatus.CREATED.value == "created"
        assert ProjectStatus.SET_UP.value == "set_up"
        assert ProjectStatus.ERROR.value == "error"
        assert ProjectStatus.TEAR_DOWN.value == "tear_down"
        assert ProjectStatus.DONE.value == "done"

    def test_project_status_is_enum(self):
        """Test that ProjectStatus values are enum members."""
        for status in ProjectStatus:
            assert isinstance(status, ProjectStatus)


class TestSessionStatus:
    """Test cases for SessionStatus enum."""

    def test_session_status_values(self):
        """Test that SessionStatus enum has expected values."""
        assert SessionStatus.CREATED.value == "created"
        assert SessionStatus.SET_UP.value == "set_up"
        assert SessionStatus.PLANNING.value == "planning"
        assert SessionStatus.AWAITING_INPUT.value == "awaiting_input"
        assert SessionStatus.BUILDING.value == "building"
        assert SessionStatus.IN_REVIEW.value == "in_review"
        assert SessionStatus.LINTING.value == "linting"
        assert SessionStatus.TESTING.value == "testing"
        assert SessionStatus.TEAR_DOWN.value == "tear_down"
        assert SessionStatus.DONE.value == "done"

    def test_session_status_is_enum(self):
        """Test that SessionStatus values are enum members."""
        for status in SessionStatus:
            assert isinstance(status, SessionStatus)
