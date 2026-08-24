from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import admin_required
from app.models.user import User

from app.schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentStatusUpdate,
)

from app.services.agent_service import (
    create_agent,
    get_agents,
    get_agent,
    update_agent,
    update_agent_status,
)

router = APIRouter(
    prefix="/admin/agents",
    tags=["Admin - Agents"],
)

#
# @router.get("/dashboard")
# def dashboard(
#     current_user: User = Depends(agent_required)
# ):
#     return {
#         "message": "Welcome Agent Dashboard",
#         "user": current_user.full_name
#     }



@router.post(
    "",
    response_model=AgentResponse,
)
def create_agent_endpoint(
    agent_data: AgentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return create_agent(db, agent_data)


@router.get(
    "",
    response_model=list[AgentResponse],
)
def list_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return get_agents(db)


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
def get_agent_endpoint(
    agent_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return get_agent(db, agent_id)


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
)
def update_agent_endpoint(
    agent_id: int,
    agent_data: AgentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return update_agent(db, agent_id, agent_data)


@router.patch(
    "/{agent_id}/status",
    response_model=AgentResponse,
)
def update_agent_status_endpoint(
    agent_id: int,
    status_data: AgentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    return update_agent_status(
        db,
        agent_id,
        status_data.is_active,
    )