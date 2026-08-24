from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.schemas.agent import AgentCreate, AgentUpdate
from app.core.security import hash_password


def get_agent_role(db: Session):
    role = db.query(Role).filter(Role.name == "AGENT").first()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AGENT role does not exist."
        )

    return role


def create_agent(db: Session, agent_data: AgentCreate):

    existing_email = db.query(User).filter(
        User.email == agent_data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    if agent_data.phone:
        existing_phone = db.query(User).filter(
            User.phone == agent_data.phone
        ).first()

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered."
            )

    agent_role = get_agent_role(db)

    agent = User(
        full_name=agent_data.full_name,
        email=agent_data.email,
        phone=agent_data.phone,
        password=hash_password(agent_data.password),
        role_id=agent_role.id,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


def get_agents(db: Session):
    return (
        db.query(User)
        .join(Role)
        .filter(Role.name == "AGENT")
        .all()
    )


def get_agent(db: Session, agent_id: int):

    agent = (
        db.query(User)
        .join(Role)
        .filter(
            User.id == agent_id,
            Role.name == "AGENT"
        )
        .first()
    )

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found."
        )

    return agent


def update_agent(
    db: Session,
    agent_id: int,
    agent_data: AgentUpdate
):

    agent = get_agent(db, agent_id)

    if agent_data.email and agent_data.email != agent.email:

        existing_email = db.query(User).filter(
            User.email == agent_data.email,
            User.id != agent_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    if agent_data.phone and agent_data.phone != agent.phone:

        existing_phone = db.query(User).filter(
            User.phone == agent_data.phone,
            User.id != agent_id
        ).first()

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered."
            )

    update_data = agent_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(agent, field, value)

    db.commit()
    db.refresh(agent)

    return agent


def update_agent_status(
    db: Session,
    agent_id: int,
    is_active: bool
):

    agent = get_agent(db, agent_id)

    agent.is_active = is_active

    db.commit()
    db.refresh(agent)

    return agent