import subprocess  # nosec
from pathlib import Path

from langchain.tools import ToolRuntime, tool

from chimera.models.context import Context
from chimera.settings import OPENCODE_PATH


@tool("plan-agent", description="Used to plan a feature implementation")
async def plan_agent(query: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return run_opencode_agent(project_path, query, agent="plan")


@tool("build-agent", description="Used to build a feature")
async def build_agent(query: str, runtime: ToolRuntime[Context]):
    project_path = runtime.context.project_path
    return run_opencode_agent(project_path, query, agent="build")


def run_opencode_agent(project_path: Path, query: str, agent: str = "plan") -> str:
    query = query + "\nFollow the instructions in the AGENTS.md for Git and Linear workflows."
    result = subprocess.run(
        [
            OPENCODE_PATH,
            "--agent",
            agent,
            "--prompt",
            query,
            "--model",
            "opencode/minimax-m2.1-free",
            "--quiet",
        ],  # nosec
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    return result.stdout
