from fastapi import APIRouter, Depends

from app.core.dependencies import user_required
from app.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(user_required)
):
    return {
        "message": "Welcome User Dashboard",
        "user": current_user.full_name
    }