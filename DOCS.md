# DOCS.md v1.0.0

## Project Overview

Chimera is an AI-powered coding workflow orchestration tool that coordinates multiple AI coding agents to automate software development tasks. It acts as a supervisor agent using LangGraph that integrates with Linear (issue tracking via MCP), and OpenCode (feature planning and building) to create a seamless development workflow.

## History

This project is the successor of [Demetra](https://github.com/manti-by/demetra), a coding workflow orchestration tool that coordinated AI agents using async subprocess calls. Chimera builds on the same idea but with a graph agent architecture powered by LangChain, LangGraph, and Groq.

### First Release (v0.3.2)

The initial release includes:
- Supervisor agent with LangGraph orchestration
- Plan, Build, and Review agent system
- Linear MCP integration for task retrieval
- OpenCode integration for AI-powered development
- Git worktree-based feature development
- Human-in-the-loop middleware for user approval
- PostgreSQL persistence with Alembic migrations
- Full test coverage with pytest

## Technical Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13 |
| Orchestration | LangChain, LangGraph |
| LLM | Groq (Llama 3.3 70b) |
| Task Tracking | Linear MCP |
| Coding Agent | OpenCode CLI |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Testing | pytest, pytest-asyncio |
| Linting | Ruff |
| Type Checking | ty |

## Requirements

- Python 3.13
- Groq API key
- Linear API key and Team ID
- OpenCode CLI
- PostgreSQL database (for state persistence)
- LangSmith API key (optional, for tracing)

## Project Structure

```
chimera/
├── main.py                 # Entry point
├── workflow.py             # LangGraph workflow orchestration
├── settings.py             # Core configuration
├── library/                # Core models and utilities
│   ├── models.py           # Data models (WorkflowState)
│   ├── types.py            # Type definitions
│   ├── parser.py           # CLI argument parsing
│   ├── exceptions.py       # Custom exceptions
│   ├── constants.py        # Constants
│   ├── header.py           # Header formatting
│   └── parser.py           # CLI parsing
├── services/               # Service integrations
│   ├── linear.py           # Linear MCP configuration
│   ├── opencode.py         # OpenCode agent service
│   ├── git.py              # Git operations
│   ├── flow.py             # Workflow orchestration
│   ├── prompt.py           # Prompt template loading
│   ├── subprocess.py       # Subprocess management
│   ├── terminal.py         # Terminal output utilities
│   ├── utils.py            # General utilities
│   ├── database.py         # Database operations
│   └── project.py          # Project management
├── tools/                  # LangGraph tool definitions
│   ├── git.py              # Git tools (worktree, commit, push, etc.)
│   ├── github.py           # GitHub PR creation
│   ├── opencode.py         # OpenCode plan/build/review tools
│   ├── lint.py             # Ruff lint and format tools
│   └── test.py             # Pytest tool
├── database/               # Database layer
│   ├── connection.py       # SQLAlchemy async connection
│   ├── tables.py           # Table definitions
│   └── migrations/         # Alembic migrations
└── prompts/                # System prompt templates
    ├── system.md           # System prompt
    ├── workflow.md         # Workflow instructions
    └── review.md           # Review agent prompt
```

## Git Workflow

This project adheres strictly to the Git Flow branching model. AI agents must follow these guidelines:

### Main Branch:

- The `master` branch always contains production-ready, stable code.
- Never commit directly to `master`.
- Do not use `git push --force` on the `master` branch.
- Do not merge branches into `master` without explicit approval.

### Feature Branches:

- Create feature branches using the naming convention `<agent-name>/feature/<issue-id>-<descriptive-name>` (e.g., `opencode/feature/CHIMERA-10-add-user-authentication`).
- Use the [Conventional Commits](https://www.conventionalcommits.org) specification for commit messages (e.g., `feat:`, `fix:`, `docs:`).
- Ensure all local tests pass before committing.
- Use `git push --force-with-lease` if needed on your feature branch, but never on `master`.

### Pull Requests (PRs):

- Open a Pull Request for every completed feature branch.
- PRs must be reviewed and pass all CI checks before merging.
- The PR title should follow the Conventional Commits specification.

## Linear Workflow

- When starting implementation of any issue from `TODO`, move it to `In Progress` column.
- When feature is completed and PR is created, move it to `In Review` column.
- After approval, merge the feature branch into `master` and move the issue to `Done` column.
- If the feature branch is not merged into `master`, move it back to `In Progress` column.
- If the feature branch is closed without merging, move it to `Closed` column.

## Development Commands

### Package Management

```bash
# Install dependencies (including dev extras)
uv sync --all-extras --dev

# Upgrade dependencies and pre-commit hooks
uv sync --upgrade --all-extras --dev
uv run pre-commit autoupdate
```

### Makefile Targets

```bash
make run-odin   # Run workflow on 'odin' project
make check      # Run type checking and pre-commit checks
make install    # Install dependencies
make update     # Upgrade dependencies and pre-commit hooks
make ci         # Shorthand: install check
```

### Running Modules

From the project root, after creating a virtualenv and installing dependencies:

```bash
uv run main.py --project-name <project_name>
```

## Language & Environment

- Python 3.13 (see `pyproject.toml`)
- Follow PEP 8 style guidelines, with Ruff enforcing style and linting (120 char line length)
- Use type hints for public functions and complex code paths
- Prefer f-strings over `.format()` or `%`
- Use list/dict/set comprehensions instead of `map`/`filter` where it improves readability
- Prefer `pathlib.Path` over `os.path` for filesystem paths
- Follow PEP 257 for docstrings where docstrings are used
- Prefer EAFP (try/except) over LBYL (if checks) in Python code

## Code Style & Tooling

Configured in `pyproject.toml`:

- **Ruff** for linting and import management (`[tool.ruff]`, `[tool.ruff.lint]`)
- **pre-commit** is used to run the tools before commits
- **ty** for type checking

Run manually:

```bash
uv run pre-commit run --all-files
uv run ruff check .
uv run ty check
```

## Testing Guidelines

- Use `pytest` with `pytest-asyncio` for async tests
- Tests are located in the `tests/` directory
- Run tests with: `uv run pytest`

## Environment & Configuration

Environment is controlled primarily via `chimera/settings.py` and `.env`:

- `LINEAR_API_KEY`: API key for Linear integration
- `LINEAR_API_URL`: Linear GraphQL API URL
- `LINEAR_TEAM_ID`: Linear team ID
- `OPENCODE_PATH`: Path to OpenCode CLI binary
- `GROQ_API_KEY`: API key for Groq (LLM)
- `GROQ_MODEL`: Groq model to use (default: llama-3.1-8b-instant)
- `LANGSMITH_TRACING`, `LANGSMITH_API_KEY`: LangSmith tracing configuration
- `DB_URL`: PostgreSQL database URL

## External Dependencies

Chimera coordinates the following external tools:

- **OpenCode**: AI coding assistant for planning and building features
- **Linear**: Issue tracking via MCP API
- **Groq**: LLM powering the supervisor agent (Llama 3.1 8B)
- **Git**: Worktree-based feature development

## Dependencies

### Core
- `aiofiles` - Async file operations
- `aiohttp` - Async HTTP client
- `alembic` - Database migrations
- `langchain` - LangChain framework
- `langchain-groq` - Groq integration
- `langchain-mcp-adapters` - MCP adapters
- `langgraph` - LangGraph workflow orchestration
- `langsmith` - LangSmith tracing
- `mcp` - Model Context Protocol
- `python-slugify` - Slugify utility
- `rich` - Rich terminal output
- `sqlalchemy` - Database ORM

### Development
- `ipython` - Interactive Python
- `ty` - Python type checker
- `pre-commit` - Git hooks
- `uv-bump` - Version bumping
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `psycopg` - PostgreSQL driver

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/chimera.yml` and runs:
- Dependency installation
- Pre-commit hooks on all files

## Security Guidelines

- Never commit secrets, passwords, or API tokens
- Configure sensitive values via environment variables
- Validate any external input before using it in system calls or network operations

## AI Behavior

Response style – concise and minimal:

- Provide minimal, working code without unnecessary explanation
- Omit comments unless essential for understanding
- Skip boilerplate and obvious patterns unless requested
- Use type inference and shorthand syntax where possible
- Focus on the core solution, skip tangential suggestions
- Assume familiarity with language idioms and patterns
- Let code speak for itself through clear naming and structure
- Avoid over-explaining standard patterns and conventions
- Provide just enough context to understand the solution
- Trust the developer to handle obvious cases independently
