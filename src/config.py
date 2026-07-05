import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 1. Base Environment Configurations
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "Benadfem"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "chopnow_db"

    # 2. Automatically computed database drivers
    @property
    def DATABASE_URL(self) -> str:
        """Standard driver URL for synchronous processes like basic scripts."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Asynchronous driver URL required by modern SQLAlchemy engines and Alembic layers."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # 3. Read configuration states directly from your root `.env` file securely
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiate a single global config instance for your entire application
settings = Settings()