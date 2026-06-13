up:
	docker compose up --build

dev:
	uv sync
	uv run alembic upgrade head
	uv run uvicorn src.app.main:app --reload

format:
	ruff format .
	ruff check --fix .