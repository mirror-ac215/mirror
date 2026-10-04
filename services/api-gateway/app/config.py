from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration supplied through environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "mirror-api-gateway"
    log_level: str = "INFO"

    # Where the other services live. The defaults are the docker-compose service
    # names: inside the compose network, containers find each other by name
    cv_service_url: str = "http://cv-service:8001"
    llm_service_url: str = "http://llm-service:8002"
    db_host: str = "db"
    db_port: int = 5432
    dependency_timeout_s: float = 2.0 
