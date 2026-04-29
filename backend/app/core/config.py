from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    ENV: str = "dev"

    DATABASE_URL: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"

    FRONT: str | None = None  # ← 追加（CORSで使う）

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache#「Settings()を毎回作らず、最初の1回だけ作ってずっと再利用する」
def get_settings() -> Settings:#無駄な生成が減る（軽いけど積もる）
    return Settings()