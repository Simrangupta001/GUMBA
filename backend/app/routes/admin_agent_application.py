from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import admin_required
from app.models.user import User
from app.schemas.agent_application import AgentApplicationAdminResponse
from app.services.agent_application_service import AgentApplicationService

router = APIRouter(
    prefix="/admin/agent-applications",
    tags=["Admin - Agent Applications"],
)


@router.get(
    "",
    response_model=List[AgentApplicationAdminResponse],
)
def list_agent_applications(
    verification_status: Optional[str] = Query(
        default=None,
        description="Filter by PENDING, APPROVED or REJECTED.",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return AgentApplicationService.get_all_applications(
        db,
        verification_status,
    )


@router.get(
    "/{application_id}",
    response_model=AgentApplicationAdminResponse,
)
def get_agent_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return AgentApplicationService.get_application_by_id(
        db,
        application_id,
    )


@router.patch(
    "/{application_id}/approve",
    response_model=AgentApplicationAdminResponse,
)
def approve_agent_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return AgentApplicationService.approve_application(
        db,
        application_id,
    )


@router.patch(
    "/{application_id}/reject",
    response_model=AgentApplicationAdminResponse,
)
def reject_agent_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return AgentApplicationService.reject_application(
        db,
        application_id,
    )