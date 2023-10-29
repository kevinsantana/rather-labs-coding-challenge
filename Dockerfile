FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY setup.py .
COPY README.md .

RUN pip install --no-cache-dir -e .

COPY . .

# final stage
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpq-dev

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/ .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 3060

CMD ["gunicorn", "--bind=0.0.0.0:3060", "--workers=3", "--worker-class=uvicorn.workers.UvicornWorker", "--timeout=174000", "product_inventory.rest.app:start_application()"]