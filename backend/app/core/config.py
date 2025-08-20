from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load .env early
load_dotenv()


class Settings(BaseSettings):
    app_name: str = Field("Text-to-SQL Backend", env="APP_NAME")
    sqlite_path: str = Field("school.db", env="SQLITE_PATH")

    # Groq (primary)
    groq_api_key: str | None = Field(default=None, env="GROQ_API_KEY")
    groq_model: str = Field("llama-3.1-70b-versatile", env="GROQ_MODEL")

    # Deprecated/unused (kept for compatibility)
    google_api_key: str | None = Field(default=None, env="GOOGLE_API_KEY")
    gemini_model: str = Field("gemini-1.5-flash", env="GEMINI_MODEL")

    # Pydantic v2 settings config
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
