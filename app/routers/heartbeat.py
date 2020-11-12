from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HearbeatResult(BaseModel):
    is_alive: bool


@router.get("/heartbeat", response_model=HearbeatResult, name="heartbeat")
def get_hearbeat() -> HearbeatResult:
    """
    Heartbeat if the service is alive.
    """

    return HearbeatResult(is_alive=True)
