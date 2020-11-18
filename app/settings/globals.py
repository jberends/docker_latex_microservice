from pathlib import Path

from starlette.config import Config
from starlette.datastructures import Secret
from typing import Optional

from __about__ import __version__

package_root: Path = Path(__file__).parent.parent / ".env"
config: Config = Config(package_root if package_root.exists() else None)

APP_NAME: str = "Latex docker microservice"
APP_VERSION: str = __version__

# Application Root. This is the directory where './app' is in.
APP_ROOT: Path = Path(__file__).parents[2]

API_PREFIX: str = config("API_PREFIX", cast=str, default="/api")

# Very simple Authentication with API KEY
API_KEY: Optional[Secret] = config("API_KEY", cast=Secret, default=None)
API_AUTHORIZATION_HEADER: str = config(
    "API_AUTHORIZATION_HEADER", cast=str, default="Token"
)

# Set to True to enable debug mode
DEBUG: bool = config("DEBUG", cast=bool, default=True)

# Sentry error logging
SENTRY_DSN: Optional[Secret] = config("SENTRY_DSN", cast=Secret, default=None)

# PDF latex settings
PDFLATEX_PATH: Path = config(
    "PDFLATEX_PATH", cast=Path, default=Path("/usr/bin/lualatex")
)
DEBUG_LOG_RENDERED_TEX: bool = config(
    "DEBUG_LOG_RENDERED_TEX", cast=bool, default=DEBUG)
PDF_WORKSPACE_BASE: Path = config(
    "PDF_WORKSPACE_BASE", cast=Path, default=APP_ROOT / 'workspace'
)


print(f"""
{PDFLATEX_PATH=}
{DEBUG=}
{SENTRY_DSN=}
{PDF_WORKSPACE_BASE=}
""")
