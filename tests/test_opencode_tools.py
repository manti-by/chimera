from unittest.mock import AsyncMock, patch

import pytest

from chimera.tools.opencode import (
    PLAN_HAS_QUESTIONS,
    PLAN_IS_READY_STRING,
    build_agent_tool,
    plan_agent_tool,
    review_agents_tool,
)


class TestPlanAgentTool:
    """Test cases for plan_agent_tool."""

    @pytest.mark.asyncio
    async def test_plan_agent_tool_calls_run_opencode_agent(self, mock_path):
        """Test that plan_agent_tool calls run_opencode_agent."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_plan_agent_tool_appends_instructions(self, mock_path):
        """Test that plan_agent_tool appends instructions to task."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert PLAN_HAS_QUESTIONS in call_kwargs["task"]
        assert PLAN_IS_READY_STRING in call_kwargs["task"]

    @pytest.mark.asyncio
    async def test_plan_agent_tool_includes_output_length_constraint(self, mock_path):
        """Test that plan_agent_tool includes output length constraint instruction."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert "4095" in call_kwargs["task"]
        assert "symbols" in call_kwargs["task"].lower() or "characters" in call_kwargs["task"].lower()
        assert "truncation" in call_kwargs["task"].lower()

    @pytest.mark.asyncio
    async def test_plan_agent_tool_uses_plan_model(self, mock_path):
        """Test that plan_agent_tool uses the plan model from settings."""
        with (
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"plan_model": "plan-model"}),
        ):
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["model"] == "plan-model"

    @pytest.mark.asyncio
    async def test_plan_agent_tool_uses_plan_agent(self, mock_path):
        """Test that plan_agent_tool uses 'plan' as agent type."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["agent"] == "plan-agent"

    @pytest.mark.asyncio
    async def test_plan_agent_tool_uses_worktree_path(self, mock_path):
        """Test that plan_agent_tool uses the worktree path."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["target_path"] == mock_path

    @pytest.mark.asyncio
    async def test_plan_agent_tool_returns_result(self, mock_path):
        """Test that plan_agent_tool returns the agent result."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "Plan output", "")

            result = await plan_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        assert result == (0, "Plan output", "")


class TestBuildAgentTool:
    """Test cases for build_agent_tool."""

    @pytest.mark.asyncio
    async def test_build_agent_tool_calls_run_opencode_agent(self, mock_path):
        """Test that build_agent_tool calls run_opencode_agent."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await build_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        mock_run.assert_called_once()

    @pytest.mark.asyncio
    async def test_build_agent_tool_appends_no_commit_instruction(self, mock_path):
        """Test that build_agent_tool appends 'no commit' instruction to task."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await build_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert "DO NOT commit" in call_kwargs["task"]

    @pytest.mark.asyncio
    async def test_build_agent_tool_uses_build_model(self, mock_path):
        """Test that build_agent_tool uses the build model from settings."""
        with (
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"build_model": "build-model"}),
        ):
            mock_run.return_value = (0, "", "")

            await build_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["model"] == "build-model"

    @pytest.mark.asyncio
    async def test_build_agent_tool_uses_build_agent(self, mock_path):
        """Test that build_agent_tool uses 'build' as agent type."""
        with patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run:
            mock_run.return_value = (0, "", "")

            await build_agent_tool.ainvoke({"task": "Test task", "worktree_path": mock_path})

        call_kwargs = mock_run.call_args.kwargs
        assert call_kwargs["agent"] == "build-agent"


class TestReviewAgentsTool:
    """Test cases for review_agents_tool."""

    @pytest.mark.asyncio
    async def test_review_agents_tool_calls_get_prompt(self, mock_path):
        """Test that review_agents_tool calls get_prompt."""
        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": ["model-1"]}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = (0, "", "")
            mock_merge.return_value = (0, "", "")

            await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        mock_prompt.assert_called_once_with(name="review_agent")

    @pytest.mark.asyncio
    async def test_review_agents_tool_runs_multiple_agents(self, mock_path):
        """Test that review_agents_tool runs multiple review agents."""
        review_models = ["model-1", "model-2", "model-3"]

        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": review_models}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = (0, "", "")
            mock_merge.return_value = (0, "", "")

            await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        # Should be called once for each review model
        assert mock_run.call_count == len(review_models)

    @pytest.mark.asyncio
    async def test_review_agents_tool_uses_review_models_from_settings(self, mock_path):
        """Test that review_agents_tool uses review models from settings."""
        review_models = ["review-model-1", "review-model-2"]

        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": review_models}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = (0, "", "")
            mock_merge.return_value = (0, "", "")

            await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        # Check that each review model is used
        called_models = [call.kwargs["model"] for call in mock_run.call_args_list]
        for model in review_models:
            assert model in called_models

    @pytest.mark.asyncio
    async def test_review_agents_tool_calls_merge_results(self, mock_path):
        """Test that review_agents_tool calls merge_review_results."""
        review_models = ["model-1"]
        agent_results = [(0, "review output", "")]

        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": review_models}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = agent_results[0]
            mock_merge.return_value = (0, "merged output", "")

            result = await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        mock_merge.assert_called_once()
        assert result == (0, "merged output", "")

    @pytest.mark.asyncio
    async def test_review_agents_tool_uses_worktree_path(self, mock_path):
        """Test that review_agents_tool uses the worktree path."""
        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": ["model-1"]}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = (0, "", "")
            mock_merge.return_value = (0, "", "")

            await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        # Check that target_path is set correctly in each call
        for call in mock_run.call_args_list:
            assert call.kwargs["target_path"] == mock_path

    @pytest.mark.asyncio
    async def test_review_agents_tool_uses_review_agent_type(self, mock_path):
        """Test that review_agents_tool uses 'review' as agent type."""
        with (
            patch("chimera.tools.opencode.get_prompt", new_callable=AsyncMock) as mock_prompt,
            patch("chimera.tools.opencode.run_opencode_agent", new_callable=AsyncMock) as mock_run,
            patch("chimera.tools.opencode.OPENCODE", {"review_models": ["model-1"]}),
            patch("chimera.tools.opencode.merge_review_results", new_callable=AsyncMock) as mock_merge,
        ):
            mock_prompt.return_value = "review task"
            mock_run.return_value = (0, "", "")
            mock_merge.return_value = (0, "", "")

            await review_agents_tool.ainvoke({"worktree_path": mock_path, "model": "model-1"})

        for call in mock_run.call_args_list:
            assert call.kwargs["agent"] == "review-agent"


class TestConstants:
    """Test cases for opencode tool constants."""

    def test_plan_header_string_exists(self):
        """Test that PLAN_HEADER_STRING is defined."""
        from chimera.tools.opencode import PLAN_HEADER_STRING

        assert isinstance(PLAN_HEADER_STRING, str)
        assert len(PLAN_HEADER_STRING) > 0

    def test_plan_is_ready_string_exists(self):
        """Test that PLAN_IS_READY_STRING is defined."""
        assert isinstance(PLAN_IS_READY_STRING, str)
        assert len(PLAN_IS_READY_STRING) > 0

    def test_plan_has_questions_exists(self):
        """Test that PLAN_HAS_QUESTIONS is defined."""
        assert isinstance(PLAN_HAS_QUESTIONS, str)
        assert len(PLAN_HAS_QUESTIONS) > 0

    def test_plan_is_ready_string_contains_ready(self):
        """Test that PLAN_IS_READY_STRING contains 'Ready'."""
        assert "Ready" in PLAN_IS_READY_STRING

    def test_plan_has_questions_contains_questions(self):
        """Test that PLAN_HAS_QUESTIONS contains 'questions'."""
        assert "questions" in PLAN_HAS_QUESTIONS.lower()
