from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.donation import Donation
from app.models.gumba import Gumba
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.services.email_service import EmailService


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

        # ---------------------------------------------------------
        # NOTIFY (after commit, so a failed/slow email can never
        # affect the fact that this status change already
        # succeeded in the database)
        # ---------------------------------------------------------

        DonationService._notify_donation_status_change(db, donation)

        return donation

    # ---------------------------------------------------------
    # EMAIL NOTIFICATIONS
    # ---------------------------------------------------------

    @staticmethod
    def _notify_donation_status_change(
        db: Session,
        donation: "Donation",
    ):
        status_label = (
            "Approved" if donation.status == "APPROVED" else "Rejected"
        )

        donor = donation.user
        gumba = donation.gumba

        amount_str = f"{donation.amount:,.2f}"
        gumba_name = gumba.name if gumba else "N/A"
        donor_name = donor.full_name if donor else "Unknown"
        banner_color = "#16a34a" if donation.status == "APPROVED" else "#dc2626"



        # ---- Donor email ----

        if donor and donor.email:
            EmailService.send_templated_email(
                to=donor.email,
                subject=f"Your donation has been {status_label.lower()}",
                template_name="donation_status.html",
                context={
                    "status": donation.status,
                    "status_label": status_label,
                    "greeting_name": donor_name,
                    "is_admin_copy": False,
                    "donation_id": donation.id,
                    "donor_name": donor_name,
                    "gumba_name": gumba_name,
                    "currency": "NPR",
                    "amount": amount_str,
                    "donation_message": donation.message,
                    "banner_color": banner_color,
                },
            )

        # ---- Admin email ----
        # Fixed recipient from .env (settings.ADMIN_EMAIL), per
        # explicit decision - not a dynamic "all ADMIN-role users"
        # lookup.

        if settings.ADMIN_EMAIL:
            EmailService.send_templated_email(
                to=settings.ADMIN_EMAIL,
                subject=(
                    f"Donation #{donation.id} has been "
                    f"{status_label.lower()}"
                ),
                template_name="donation_status.html",
                context={
                    "status": donation.status,
                    "status_label": status_label,
                    "greeting_name": "Admin",
                    "is_admin_copy": True,
                    "donation_id": donation.id,
                    "donor_name": donor_name,
                    "gumba_name": gumba_name,
                    "currency": "NPR",
                    "amount": amount_str,
                    "donation_message": donation.message,
                    "banner_color": banner_color,
                },
            )