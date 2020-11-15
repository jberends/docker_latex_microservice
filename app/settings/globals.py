from pathlib import Path

from starlette.config import Config
from starlette.datastructures import Secret
from typing import Optional

from app.__about__ import __version__

p: Path = Path(__file__).parents[2] / ".env"
config: Config = Config(p if p.exists() else None)

APP_NAME: str = "Latex docker microservice"
APP_VERSION: str = __version__
API_PREFIX: str = config("API_PREFIX", cast=str, default="/api")
API_KEY: Optional[Secret] = config("API_KEY", cast=Secret, default=None)
DEBUG: bool = config("DEBUG", cast=bool, default=True)

PDFLATEX_PATH: Path = config(
    "PDFLATEX_PATH", cast=Path, default=Path("/usr/bin/lualatex")
)
DEBUG_LOG_RENDERED_TEX: bool = config(
    "DEBUG_LOG_RENDERED_TEX", cast=bool, default=True)

SENTRY_DSN: Optional[Secret] = config("SENTRY_DSN", cast=Secret, default=None)
