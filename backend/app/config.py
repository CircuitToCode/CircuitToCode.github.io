from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "Nityanand Portfolio API"
    environment: str = "development"
    database_url: str = "sqlite:///./portfolio.db"
    jwt_secret: str
    jwt_expire_minutes: int = 60
    admin_username: str = "admin"
    admin_password_hash: str
    cors_origins: str = "http://localhost:5173,https://circuittocode.github.io"
    upload_dir: str = "uploads"
    max_upload_mb: int = 10
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

@lru_cache
def get_settings() -> Settings:
    return Settings()
