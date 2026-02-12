# Chimera

Chimera is an AI-powered coding workflow orchestration tool that coordinates multiple AI coding agents to automate software development tasks. It acts as a supervisor agent that integrates with Linear (issue tracking), OpenCode (feature planning and building), and CodeRabbit (code review) to create a seamless development workflow.

## Features

- **Supervisor Agent**: Orchestrates the entire development workflow
- **Linear Integration**: Retrieves tasks from Linear issue tracker
- **OpenCode Integration**: Plans and builds features using OpenCode agents
- **CodeRabbit Integration**: Reviews code changes with AI-powered feedback
- **Multi-Agent Coordination**: Coordinates between planning, building, and review agents

## Architecture

```
User Request
      │
      ▼
┌─────────────────────────────────┐
│         Supervisor Agent        │  (Groq - Llama 3.1 8B)
│   (Chimera Main Controller)     │
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
│    (Planning & Building Tasks)  │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│           CodeRabbit            │
│       (Code Review Agent)       │
└─────────────────────────────────┘
```

## Workflow

1. **Task Retrieval**: Fetch the latest task from Linear (TODO column)
2. **Planning**: Create an implementation plan using OpenCode's plan agent
3. **User Approval**: Wait for user input to proceed
4. **Building**: Implement the feature using OpenCode's build agent
5. **Review**: Check the feature using CodeRabbit
6. **Iteration**: If issues are found, return to previous steps for fixes

## Requirements

- Python 3.13
- Groq API key
- Linear API key and Team ID
- OpenCode CLI
- CodeRabbit CLI
- LangSmith API key (for tracing)

## Installation

```bash
uv sync --all-extras --dev
```

## Configuration

Configure the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJECTS_PATH` | Path to projects directory | `$HOME/www` |
| `LINEAR_API_KEY` | Linear API key | - |
| `LINEAR_API_URL` | Linear GraphQL API URL | `https://api.linear.app/graphql` |
| `LINEAR_TEAM_ID` | Linear team ID | - |
| `OPENCODE_PATH` | Path to OpenCode binary | `$HOME/.opencode/bin/opencode` |
| `CODERABBIT_PATH` | Path to CodeRabbit binary | `$HOME/.local/bin/coderabbit` |
| `LANGSMITH_TRACING` | Enable LangSmith tracing | - |
| `LANGSMITH_API_KEY` | LangSmith API key | - |
| `GROQ_API_KEY` | Groq API key | - |
| `HUGGINGFACEHUB_API_TOKEN` | HuggingFace token | - |

## Usage

Run Chimera for a specific project:

```bash
uv run main.py --project-name <project_name>
```

Available make commands:

```bash
# Run workflow on 'odin' project
make run-odin

# Run type checking and pre-commit checks
make check

# Install dependencies
make pip

# Update dependencies
make update

# CI check
make ci
```

## Project Structure

```
chimera/
├── __init__.py
├── models/
│   └── context.py              # Context dataclass for agent state
├── services/
│   ├── __init__.py
│   ├── coderabbit.py           # CodeRabbit review agent integration
│   ├── filesystem.py           # Project filesystem utilities
│   ├── graphql.py              # GraphQL client for Linear API
│   ├── linear.py               # Linear task retrieval
│   ├── opencode.py             # OpenCode plan/build agents
│   ├── prompt.py               # Prompt template loading
│   ├── prompts/
│   │   ├── system.md           # System prompt for supervisor
│   │   └── workflow.md         # Workflow template
│   └── queries/
│       └── get_todo_issues.gql # GraphQL query for Linear issues
├── settings.py                 # Settings and configuration
└── main.py                     # Entry point and supervisor agent
```

## Dependencies

### Core
- `asyncio` - Asynchronous programming
- `deepagents` - Agent framework
- `aiofiles` - Async file operations
- `aiohttp` - Async HTTP client
- `langchain-groq` - Groq integration
- `mcp` - Model Context Protocol

### Development
- `ipython` - Interactive Python
- `ty` - Python type checker
- `pre-commit` - Git hooks
- `uv-bump` - Version bumping

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/checks.yml` and runs:
- Dependency installation
- Pre-commit hooks on all files

## License

BSD 3-Clause License
