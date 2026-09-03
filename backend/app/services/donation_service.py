from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.gumba import Gumba
from app.models.user import User
from app.schemas.donation import DonationCreate


class DonationService:

    @staticmethod
    def create_donation(
        db: Session,
        user: User,
        donation_data: DonationCreate
    ):

        # Check that the Gumba exists and is active
        gumba = (
            db.query(Gumba)
            .filter(
                Gumba.id == donation_data.gumba_id,
                Gumba.is_active == True
            )
            .first()
        )

        if gumba is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gumba not found."
            )

        donation = Donation(
            user_id=user.id,
            gumba_id=donation_data.gumba_id,
            amount=donation_data.amount,
            message=donation_data.message,
            anonymous=donation_data.anonymous,
            status="PENDING"
        )

        db.add(donation)
        db.commit()
        db.refresh(donation)

        return donation

    @staticmethod
    def get_user_donations(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Donation)
            .filter(
                Donation.user_id == user_id
            )
            .order_by(Donation.id.desc())
            .all()
        )

    @staticmethod
    def get_agent_donations(
        db: Session,
        agent_id: int
    ):
        return (
            db.query(Donation)
            .join(Gumba, Donation.gumba_id == Gumba.id)
            .filter(
                Gumba.agent_id == agent_id,
                Donation.is_active == True
            )
            .order_by(Donation.id.desc())
            .all()
        )

    @staticmethod
    def update_donation_status(
        db: Session,
        donation_id: int,
        agent_id: int,
        new_status: str
    ):
        donation = (
            db.query(Donation)
            .join(Gumba, Donation.gumba_id == Gumba.id)
            .filter(
                Donation.id == donation_id,
                Gumba.agent_id == agent_id,
                Donation.is_active == True
            )
            .first()
        )

        if donation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Donation not found or you are not assigned to this Gumba."
            )

        if donation.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending donations can be verified."
            )

        donation.status = new_status

        db.commit()
        db.refresh(donation)

        return donation

    