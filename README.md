# Chimera

AI-powered coding workflow orchestration tool that coordinates AI agents (Linear, OpenCode) via a supervisor agent (Groq llama-3.3-70b-versatile) using LangGraph.

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
