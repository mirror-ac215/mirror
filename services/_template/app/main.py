from uuid import uuid4

from fastapi import FastAPI, Request, Response

from app.config import Settings
from app.logging_config import configure_logging, request_id_context

settings = Settings()
logger = configure_logging(settings.log_level)

app = FastAPI(title=settings.app_name)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    token = request_id_context.set(request_id)

    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "request_completed",
            extra={"path": request.url.path, "status_code": response.status_code},
        )
        return response
    finally:
        request_id_context.reset(token)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> Response:
    """Placeholder for service-specific metrics added by each component owner."""

    return Response(
        content="# Service-specific metrics are added by each component owner.\n",
        media_type="text/plain; version=0.0.4",
    )
