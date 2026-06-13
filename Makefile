app:
	docker compose up --build

format:
	ruff format .
	ruff check --fix .