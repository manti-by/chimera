import asyncio
from pathlib import Path

from langchain.tools import tool

from chimera.services.opencode import run_opencode_agent
from chimera.services.prompt import get_prompt
from chimera.services.utils import merge_review_results
from chimera.settings import OPENCODE


PLAN_HEADER_STRING = "## Implementation Plan"
PLAN_IS_READY_STRING = "Ready to proceed to build."
PLAN_HAS_QUESTIONS = "Please check my questions above."


@tool("plan-agent-tool", description="Opencode agent used to plan a feature implementation")
async def plan_agent_tool(task: str, worktree_path: Path) -> tuple[int, str, str]:
    task += (
        f"\nIMPORTANT:"
        f"\n- If you have some question about implementation, just print in the end `{PLAN_HAS_QUESTIONS}`"
        f"\n- If there are no questions, just print in the end `{PLAN_IS_READY_STRING}`"
    )
    return await run_opencode_agent(
        target_path=worktree_path,
        task=task,
        model=OPENCODE["plan_model"],
        agent="plan",
    )


@tool("build-agent-tool", description="Opencode agent used to build a feature")
async def build_agent_tool(task: str, worktree_path: Path) -> tuple[int, str, str]:
    task += "\nDO NOT commit or push any changes, just stage them"
    return await run_opencode_agent(
        target_path=worktree_path,
        task=task,
        model=OPENCODE["build_model"],
        agent="build",
    )


@tool("review-agents-tool", description="Opencode agents used to review a feature")
async def review_agents_tool(worktree_path: Path, model: str) -> tuple[int, str, str]:
    task = await get_prompt(name="review_agent")
    review_agents = []
    for model in OPENCODE["review_models"]:
        review_agents.append(
            run_opencode_agent(
                target_path=worktree_path,
                task=task,
                model=model,
                agent="build",
            )
        )
    results = await asyncio.gather(*review_agents)
    return await merge_review_results(results=results)
