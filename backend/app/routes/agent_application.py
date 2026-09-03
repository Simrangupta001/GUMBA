from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import user_required
from app.models.user import User

from app.schemas.agent_application import (
    AgentApplicationCreate,
    AgentApplicationResponse
)

from app.services.agent_application_service import (
    AgentApplicationService
)


router = APIRouter(
    prefix="/agent-applications",
    tags=["Agent Applications"]
)


@router.post(
    "",
    response_model=AgentApplicationResponse
)
def create_agent_application(
    application_data: AgentApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):
    return AgentApplicationService.create_application(
        db,
        current_user,
        application_data
    )