from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import user_required
from app.models.user import User

from app.schemas.donation import (
    DonationCreate,
    DonationResponse,
    DonationStatusUpdate
)

from app.services.donation_service import DonationService

from app.core.dependencies import user_required, agent_required




router = APIRouter(
    prefix="/donations",
    tags=["Donations"]
)


@router.post(
    "",
    response_model=DonationResponse
)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    return DonationService.create_donation(
        db,
        current_user,
        donation
    )


@router.get(
    "/my-donations",
    response_model=List[DonationResponse]
)
def get_my_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(user_required)
):

    return DonationService.get_user_donations(
        db,
        current_user.id
    )

@router.get(
    "/agent",
    response_model=List[DonationResponse]
)
def get_agent_donations(
    db: Session = Depends(get_db),
    current_user: User = Depends(agent_required)
):
    return DonationService.get_agent_donations(
        db,
        current_user.id
    )


@router.patch(
    "/agent/{donation_id}/status",
    response_model=DonationResponse
)
def update_donation_status(
    donation_id: int,
    status_data: DonationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(agent_required)
):
    return DonationService.update_donation_status(
        db,
        donation_id,
        current_user.id,
        status_data.status
    )