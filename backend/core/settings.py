from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


class Settings(BaseSettings):
    app_name: str = Field(default="AI SLA Intelligence Dashboard")
    api_key: str = Field(default="")
    max_upload_mb: int = Field(default=20)

    model_config = SettingsConfigDict(env_file=str(ROOT_DIR / ".env"), extra="ignore")


settings = Settings()
