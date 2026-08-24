from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import super_admin_required
from app.models.user import User
from app.schemas.admin import AdminCreate, AdminResponse, AdminUpdate, AdminStatusUpdate
from app.services.super_admin_service import SuperAdminService
from typing import List



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

@router.get(
    "/admins/{admin_id}",
    response_model=AdminResponse
)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):
    return SuperAdminService.get_admin_by_id(
        db,
        admin_id
    )

@router.put(
    "/admins/{admin_id}",
    response_model=AdminResponse
)
def update_admin(
    admin_id: int,
    admin_data: AdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):
    return SuperAdminService.update_admin(
        db,
        admin_id,
        admin_data
    )

@router.patch(
    "/admins/{admin_id}/status",
    response_model=AdminResponse
)
def update_admin_status(
    admin_id: int,
    status_data: AdminStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(super_admin_required)
):
    return SuperAdminService.update_admin_status(
        db,
        admin_id,
        status_data
    )

