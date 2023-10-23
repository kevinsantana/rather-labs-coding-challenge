include .env

run-local:
	cd product_inventory/rest && gunicorn --workers=1 --worker-class=uvicorn.workers.UvicornWorker --timeout=174000 --reload --bind=0.0.0.0:3060 'app:start_application()'
