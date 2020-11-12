from pathlib import Path

from starlette.config import Config
from starlette.datastructures import Secret

# TODO: refactor according to https://fastapi.tiangolo.com/advanced/settings/?h=+config


APP_NAME = "Latex docker microservice"
API_PREFIX = "/api"

config = Config("../.env")

API_KEY: Secret = config("API_KEY", cast=Secret)
DEBUG: bool = config("DEBUG", cast=bool, default=False)

PDFLATEX_PATH: Path = config(
    "PDFLATEX_PATH", cast=Path, default=Path("/usr/bin/lualatex")
)
DEBUG_LOG_RENDERED_TEX: bool = config(
    "DEBUG_LOG_REDENRED_TEX", cast=bool, default=False
)
