from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.agent_application import AgentApplication
from app.models.user import User
from app.schemas.agent_application import AgentApplicationCreate


class AgentApplicationService:

    @staticmethod
    def create_application(
        db: Session,
        current_user: User,
        application_data: AgentApplicationCreate
    ):

        # User must currently be a normal USER
        if current_user.role.name != "USER":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only users can apply to become an agent."
            )

        # Check whether this user already has an application
        existing_application = (
            db.query(AgentApplication)
            .filter(
                AgentApplication.user_id == current_user.id
            )
            .first()
        )

        if existing_application:

            if existing_application.verification_status == "PENDING":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You already have a pending agent application."
                )

            if existing_application.verification_status == "APPROVED":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Your agent application has already been approved."
                )

            # REJECTED
            # Allow the user to submit again.
            db.delete(existing_application)
            db.flush()

        # Make sure the identity information belongs to
        # the currently logged-in user.
        if application_data.email != current_user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email does not match the logged-in user."
            )

        if application_data.phone != current_user.phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number does not match the logged-in user."
            )

        if application_data.full_name.strip() != current_user.full_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name does not match the logged-in user."
            )

        application = AgentApplication(
            user_id=current_user.id,
            profile_photo=application_data.profile_photo,
            gender=application_data.gender,
            address=application_data.address,
            district=application_data.district,
            municipality=application_data.municipality,
            ward_no=application_data.ward_no,
            designation=application_data.designation,
            short_bio=application_data.short_bio,
            id_type=application_data.id_type,
            id_number=application_data.id_number,
            id_document=application_data.id_document,
            gumba_association_letter=application_data.gumba_association_letter,
            verification_status="PENDING"
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return application