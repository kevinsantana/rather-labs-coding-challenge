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
	cd product_inventory/rest && gunicorn --workers=1 --worker-class=uvicorn.workers.UvicornWorker --timeout=174000 --reload --bind=0.0.0.0:3060 'app:start_application()'
