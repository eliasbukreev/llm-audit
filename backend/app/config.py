from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "0.0.0.0"
    port: int = 8000

    openrouter_api_url: str = "https://openrouter.ai/api/v1/chat/completions"
    openrouter_api_key: str = ""
    llm_model: str = "openai/deepseek-r1:free"

    docs_dir: Path = BASE_DIR.parent.parent / "docs"
    results_dir: Path = BASE_DIR.parent.parent / "results"
    repos_dir: Path = BASE_DIR.parent.parent / "repos-for-analysis"
    db_path: Path = BASE_DIR / "audit.db"
    schema_path: Path = BASE_DIR.parent / "db" / "schema.sql"


settings = Settings()
