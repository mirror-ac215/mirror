# api-gateway

The only service the frontend calls. v0 (MS2): every endpoint from `docs/contracts/api-gateway.openapi.yaml` exists with the right shapes and status codes, but returns fake data. The real CV call, safety check, fusion and LLM call arrive in MS3.

## Run locally

```bash
uv sync
uv run uvicorn app.main:app --port 8000 --reload
```

Interactive API docs: http://localhost:8000/docs. Click **Authorize** and enter `dev-patient-token` (or `dev-clinician-token`).

## Endpoints (v0)

| Endpoint | Returns |
|---|---|
| `GET /health` | `ok` / `degraded` + each dependency (`cv-service`, `llm-service`, `db`); always 200 so Docker doesn't restart the gateway when a dependency is down |
| `POST /auth/login` | demo token; any email containing "clinician" logs in as clinician (real auth: M4-02) |
| `POST /sessions` | 201, in-memory session (database: MS3) |
| `POST /sessions/{id}/frames` | 202; frame read and discarded, never stored; 409 without camera consent |
| `POST /sessions/{id}/messages` | Server-Sent Events: `token` events (`{"text": ...}`) then `done` |

Errors: 401 no/invalid token, 403 wrong role, 404 unknown session, 409 no camera consent, 422 malformed request.

## Configuration (environment variables)

| Variable | Default |
|---|---|
| `CV_SERVICE_URL` | `http://cv-service:8001` |
| `LLM_SERVICE_URL` | `http://llm-service:8002` |
| `DB_HOST` / `DB_PORT` | `db` / `5432` |
| `DEPENDENCY_TIMEOUT_S` | `2.0` |
| `CORS_ORIGINS` | `["http://localhost:3000","http://localhost:8080"]` |

Defaults use docker-compose service names. No secrets needed in v0.

## Checks

```bash
uv run ruff check .
uv run pytest -q
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
