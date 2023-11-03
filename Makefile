include .env

envs:
	export $(grep -v '^#' .env | xargs)

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

migrate-up:
	cd db && alembic upgrade head

migrate-down:
	cd db && alembic downgrade -1

run-local:
	uvicorn product_inventory.rest.app:start_application --reload --host 0.0.0.0 --port 3060  --workers=1
