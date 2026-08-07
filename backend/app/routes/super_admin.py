from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import super_admin_required
from app.models.user import User
from app.schemas.admin import AdminCreate
from app.services.super_admin_service import SuperAdminService
from typing import List
from app.schemas.admin import AdminResponse


router = APIRouter(
    prefix="/super-admin",
    tags=["Super Admin"]
)

@router.post("/admins")
def create_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    new_admin = SuperAdminService.create_admin(
        db,
        admin
    )

    return {
        "message": "Admin created successfully",
        "id": new_admin.id,
        "email": new_admin.email
    }

@router.get(
    "/admins",
    response_model=List[AdminResponse]
)
def get_admins(
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):

    return SuperAdminService.get_all_admins(db)