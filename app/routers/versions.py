from ..__about__ import __version__
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class VersionResult(BaseModel):
    version: str


@router.get("/version", response_model=VersionResult, name="version")
def get_version() -> VersionResult:
    """
    Version of the application.
    """
    return VersionResult(version=__version__)
