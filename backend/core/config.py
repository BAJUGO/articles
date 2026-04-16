from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    db_url: str
    echo: bool = True

    postgres_password: str
    postgres_user: str
    postgres_db: str

    redis_host: str
    redis_port: int
    redis_password: str
    redis_db: str


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )


settings = Settings()

print(settings.db_url)