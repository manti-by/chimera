# Chimera

AI-powered coding workflow orchestration tool that coordinates multiple AI agents (Linear, OpenCode, CodeRabbit) via a supervisor agent (Groq Llama 3.1 8B).

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
│         Supervisor Agent        │  (Groq - Llama 3.1 8B)
└───────────┬─────────────────────┘
            │
    ┌───────┼───────┬────────────────┐
    │       │       │                │
    ▼      ▼       ▼                ▼
┌──────┐ ┌──────┐ ┌──────┐         Linear
│Plan  │ │Build │ │Review│      GraphQL API
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
│           CodeRabbit            │
└─────────────────────────────────┘
```

## Workflow

1. **Task Retrieval**: Fetch task from Linear (TODO column)
2. **Planning**: Create implementation plan via OpenCode
3. **User Approval**: Wait for user input
4. **Building**: Implement feature via OpenCode
5. **Review**: Check with CodeRabbit
6. **Iteration**: Loop if issues found

## Configuration

| Variable | Description |
|----------|-------------|
| `PROJECTS_PATH` | Projects directory (`$HOME/www`) |
| `LINEAR_API_KEY` | Linear API key |
| `LINEAR_TEAM_ID` | Linear team ID |
| `GROQ_API_KEY` | Groq API key |
| `OPENCODE_PATH` | OpenCode binary path |
| `CODERABBIT_PATH` | CodeRabbit binary path |

## Make Commands

```bash
make run-odin   # Run workflow on 'odin' project
make check      # Run type checking & pre-commit
make ci         # Full CI check
```

## More Info

See [DOCS.md](DOCS.md) for detailed developer documentation.

## License

BSD 3-Clause License