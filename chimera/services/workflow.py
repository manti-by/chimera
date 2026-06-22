from pathlib import Path
from typing import Any

from chimera.library.models import WorkflowState
from chimera.services.terminal import print_message
from chimera.tools.opencode import PLAN_HAS_QUESTIONS, PLAN_HEADER_STRING, PLAN_IS_READY_STRING


async def handle_build_agent(state: WorkflowState, observation: Any) -> dict[str, Any]:
    updates = {"build_attempts": state.build_attempts + 1}
    print_message(f"[tool_node/async] build_attempts: {state.build_attempts} -> {updates['build_attempts']}")
    return updates


async def handle_review_agents(state: WorkflowState, observation: Any) -> dict[str, Any]:
    updates = {"review_attempts": state.review_attempts + 1}
    print_message(f"[tool_node/async] review_attempts: {state.review_attempts} -> {updates['review_attempts']}")
    review_text = str(observation).lower()
    if any(word in review_text for word in ["issue", "error", "fix", "problem", "fail"]):
        updates["needs_rebuild"] = True
        print_message("[tool_node/async] Review found issues, setting needs_rebuild=True")
    else:
        print_message("[tool_node/async] Review passed")
    return updates


async def handle_plan_agent(state: WorkflowState, observation: Any) -> dict[str, Any]:
    updates = {}
    plan_text = str(observation)
    if PLAN_HAS_QUESTIONS in plan_text:
        print_message("[tool_node/async] Plan has questions, waiting for user input")
    elif PLAN_HEADER_STRING in plan_text:
        header_idx = plan_text.index(PLAN_HEADER_STRING)
        plan_content = plan_text[header_idx + len(PLAN_HEADER_STRING) :].strip()
        if PLAN_IS_READY_STRING in plan_content:
            plan_content = plan_content.replace(PLAN_IS_READY_STRING, "").strip()
        updates["implementation_plan"] = plan_content
        updates["needs_rebuild"] = False
        print_message(f"[tool_node/async] Extracted implementation plan, length: {len(plan_content)}")
    return updates


async def handle_git_worktree_create(state: WorkflowState, observation: Any) -> dict[str, Any]:
    updates = {}
    if not str(observation).startswith("Error:"):
        try:
            updates["worktree_path"] = Path(str(observation))
            print_message(f"[tool_node/async] Stored worktree_path: {updates['worktree_path']}")
        except (ValueError, TypeError):
            print_message("[tool_node/async] Could not parse worktree_path")
    return updates


async def handle_lint_test(state: WorkflowState, tool_name: str, observation: Any) -> dict[str, Any]:
    updates = {}
    if not str(observation).startswith("Error:"):
        updates["needs_relint"] = False
        print_message(f"[tool_node/async] {tool_name} passed, setting needs_relint=False")
    else:
        updates["needs_rebuild"] = True
        print_message(f"[tool_node/async] {tool_name} failed, setting needs_rebuild=True")
    return updates
