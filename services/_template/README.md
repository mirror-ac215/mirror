# Mirror Python service template

A copyable baseline for Mirror's Python/FastAPI services. It uses Python 3.11 and `uv`, exposes health and metrics endpoints, reads configuration from environment variables, emits JSON logs, and includes tests plus a Docker image.

## Included baseline

- FastAPI application
- `GET /health` returning `{"status":"ok"}`
- `GET /metrics` placeholder for service-specific metrics
- `X-Request-ID` propagation: preserves an inbound value or generates one, returns it in the response, and includes it in application logs
- JSON log lines for completed HTTP requests
- `pydantic-settings` configuration via environment variables
- pytest and Ruff
- Dockerfile with a Docker health check

## Prerequisites

- Docker Desktop
- `uv` (it installs the pinned Python 3.11 interpreter when necessary)

## Run locally

```bash
uv sync
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In a second terminal:

```bash
curl --fail --silent --show-error http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Interactive API documentation is available at <http://localhost:8000/docs>.

## Quality checks

```bash
uv run ruff check .
uv run pytest -v
```

## Configuration

Copy `.env.example` to `.env` only for local overrides:

```bash
cp .env.example .env
```

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `mirror-service-template` | FastAPI application title |
| `LOG_LEVEL` | `INFO` | Application log severity |

Never commit `.env`, passwords, API keys, model weights, or other secrets.

## Docker

Build from this directory:

```bash
docker build -t mirror-service-template .
```

Run the image:

```bash
docker run --rm -p 8000:8000 mirror-service-template
```

Verify the required health endpoint from a second terminal:

```bash
curl --fail --silent --show-error http://localhost:8000/health
```

The image defines a Docker `HEALTHCHECK` for the same endpoint.

## Copy this template for a new service

From the repository root:

```bash
cp -R services/_template services/<your-service-name>
cd services/<your-service-name>
```

Then the service owner must:

1. Change the project `name` and default `APP_NAME`.
2. Choose and document the service port; update the Dockerfile if it is not `8000`.
3. Replace the `/metrics` placeholder with service-specific metrics.
4. Add endpoints, tests, environment variables, Docker Compose configuration, and a CI job for the service.
5. Run `uv lock` after dependency changes and commit both `pyproject.toml` and `uv.lock`.
6. Update this README with the new service's purpose, inputs, outputs, run steps, environment variables, and required secrets.

Keep `/health`, JSON logging, request ID propagation, the Python 3.11 pin, and the no-secrets policy.
