# Chimera v1.0.0

AI-powered coding workflow orchestration tool that coordinates multiple AI coding agents via a supervisor agent (Groq Llama 3.3 70b) using LangGraph.

This project is the successor of [Demetra](https://github.com/manti-by/demetra), a coding workflow orchestration tool that coordinated AI agents using async subprocess calls and "classic" python
step-by-step loops.

## Key Features

- **Supervisor Agent**: Orchestrates workflow using Groq Llama via LangGraph
- **Multi-Agent System**: Plan, Build, and Review agents coordinated by supervisor
- **Linear Integration**: Task retrieval via MCP API
- **OpenCode Integration**: AI-powered planning and building in isolated Git worktrees
- **Human-in-the-Loop**: User approval for questions during implementation
- **Automated Workflow**: Task → Plan → Build → Review → Lint → Test → Commit → PR
- **Database Persistence**: PostgreSQL with Alembic migrations

## Quick Start

```bash
uv sync --all-extras --dev
uv run main.py --project-name <project_name>
```

## Architecture

```
User Request
      │
      ▼
┌─────────────────────────────────┐
│         Supervisor Agent        │  (Groq - Llama 3.3 70b)
│          (LangGraph)            │
└───────────┬─────────────────────┘
            │
    ┌───────┼───────┬────────────────┐
    │       │       │                │
    ▼      ▼       ▼                ▼
┌──────┐ ┌──────┐ ┌──────┐         Linear
│Plan  │ │Build │ │Review│        MCP API
│Agent │ │Agent │ │Agent │
└┬─────┘ └──┬───┘ └──┬───┘
   │        │        │
   ▼       ▼       ▼
┌─────────────────────────────────┐
│            OpenCode             │
└─────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────┐
│      Git (worktree-based)       │
└─────────────────────────────────┘
```

## Workflow

1. **Task Retrieval**: Fetch task from Linear via MCP
2. **Planning**: Create implementation plan via OpenCode
3. **User Approval**: Wait for user input if questions arise
4. **Building**: Implement feature using OpenCode in isolated worktree
5. **Review**: Check with OpenCode review agent
6. **Verification**: Run lint (ruff) and tests (pytest)
7. **Commit & PR**: Create commit, push, and open PR

## Configuration

| Variable | Description |
|----------|-------------|
| `LINEAR_API_KEY` | Linear API key |
| `LINEAR_TEAM_ID` | Linear team ID |
| `GROQ_API_KEY` | Groq API key |
| `OPENCODE_PATH` | OpenCode binary path |

## Make Commands

```bash
make run-demetra  # Run workflow on 'demetra' project
make check        # Run type checking & pre-commit
make ci           # Full CI check
```

## More Info

See [DOCS.md](DOCS.md) for detailed developer documentation.

## License

AGPL-3.0 license
