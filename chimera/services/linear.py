from langchain.tools import ToolRuntime, tool

from chimera.models.context import Context
from chimera.services.graphql import get_todo_issues_query, graphql_request
from chimera.settings import LINEAR_TEAM_ID


async def get_todo_issues(team_name: str, project_name: str) -> list[dict]:
    """Get issues from TODO column for a project ordered by priority desc and createdAt desc."""
    query = await get_todo_issues_query()
    result = await graphql_request(query, {"teamId": LINEAR_TEAM_ID})
    states = result.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])

    todo_issues = []
    for state in states:
        if state["name"].lower() == "todo":
            for issue in state["issues"]["nodes"]:
                if issue.get("project", {}).get("name", "").lower() == project_name.lower():
                    todo_issues.append(
                        {
                            "id": issue["id"],
                            "title": issue["title"],
                            "priority": issue["priority"],
                            "created_at": issue["createdAt"],
                            "description": issue.get("description", ""),
                            "state": issue["state"]["name"],
                        }
                    )
    return sorted(todo_issues, key=lambda x: (x["priority"] or 0, x["created_at"] or ""), reverse=True)


@tool("linear-task", description="Retrieve the highest priority task from Linear TODO column for the current project")
async def get_linear_task(task: str, runtime: ToolRuntime[Context]) -> str | None:
    project_name = runtime.context.project_name
    if issues := await get_todo_issues(project_name, project_name):
        return issues[0]["title"] + "\n" + issues[0]["description"]
    return None
