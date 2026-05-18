run-demetra:
	uv run main.py --project-name demetra

check:
	git add .
	uv run ty check
	uv run pre-commit run

install:
	uv sync --all-extras --dev

update:
	uv run uv-bump
	uv sync --all-extras --dev
	uv run pre-commit autoupdate

migrate:
	alembic upgrade head

ci: install check
