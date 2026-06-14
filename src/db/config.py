from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    DB_USER: str = Field(..., validation_alias="POSTGRES_USER")
    DB_PASSWORD: str = Field(..., validation_alias="POSTGRES_PASSWORD")
    DB_HOST: str = Field("localhost", validation_alias="POSTGRES_HOST")
    DB_PORT: int = Field(5432, validation_alias="POSTGRES_PORT")
    DB_NAME: str = Field(..., validation_alias="POSTGRES_DB")

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Dynamically assembles the fully compliant asyncpg connection string."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

db_settings = DatabaseSettings()