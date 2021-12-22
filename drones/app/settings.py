from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    project_name: str
    database_dsn: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
