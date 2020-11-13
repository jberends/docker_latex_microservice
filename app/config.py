from pathlib import Path

from pydantic import BaseSettings
from starlette.datastructures import Secret


class Settings(BaseSettings):
    APP_NAME: str = "Latex docker microservice"
    API_PREFIX: str = "/api"
    API_KEY: Secret = None
    DEBUG: bool = True

    PDFLATEX_PATH: Path = Path("/usr/bin/lualatex")
    DEBUG_LOG_RENDERED_TEX: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
