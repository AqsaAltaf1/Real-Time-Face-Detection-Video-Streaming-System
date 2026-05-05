from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Face Detection Streaming Backend"
    database_url: str = "postgresql://app_user:app_pass@postgres:5432/face_stream"
    allowed_origins: list[str] = ["http://localhost:5173"]
    max_frame_payload_chars: int = 2_000_000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
