from fastapi import APIRouter, Depends

from app.core.dependencies import agent_required
from app.models.user import User

router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(agent_required)
):
    return {
        "message": "Welcome Agent Dashboard",
        "user": current_user.full_name
    }