from app.config import Settings


def test_settings_have_safe_defaults() -> None:
    settings = Settings()

    assert settings.app_name == "mirror-service-template"
    assert settings.log_level == "INFO"
