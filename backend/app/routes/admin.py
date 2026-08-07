from fastapi import APIRouter, Depends

from app.core.dependencies import admin_required
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(admin_required)
):
    return {
        "message": "Welcome Admin Dashboard",
        "user": current_user.full_name
    }