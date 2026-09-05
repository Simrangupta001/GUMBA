from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.agent_application import AgentApplication
from app.models.gumba import Gumba
from app.models.user import User
from app.schemas.agent_application import AgentApplicationCreate
from app.enums.agent_application import GumbaApplicationType


class AgentApplicationService:

    @staticmethod
    def create_application(
        db: Session,
        current_user: User,
        application_data: AgentApplicationCreate,
        profile_photo: str | None = None,
        id_document: str | None = None,
        gumba_association_letter: str | None = None,
    ):

        # ---------------------------------------------------------
        # 1. ONLY NORMAL USERS CAN APPLY
        # ---------------------------------------------------------

        if current_user.role.name != "USER":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only users can apply to become an agent."
            )

        # ---------------------------------------------------------
        # 2. REQUIRED FILE REFERENCES
        # ---------------------------------------------------------

        if not id_document:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID document is required."
            )

        if not gumba_association_letter:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gumba association letter is required."
            )

        # ---------------------------------------------------------
        # 3. CHECK EXISTING APPLICATION
        # ---------------------------------------------------------

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

            # -----------------------------------------------------
            # REJECTED APPLICATION
            # -----------------------------------------------------
            #
            # Reuse the existing application record instead of
            # creating unlimited application records for one user.
            #

            application = existing_application

        else:

            application = AgentApplication(
                user_id=current_user.id
            )

        # ---------------------------------------------------------
        # 4. EXISTING GUMBA
        # ---------------------------------------------------------

        if (
            application_data.gumba_application_type
            == GumbaApplicationType.EXISTING
        ):

            if application_data.gumba_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Gumba ID is required when selecting an existing Gumba."
                )

            gumba = (
                db.query(Gumba)
                .filter(
                    Gumba.id == application_data.gumba_id,
                    Gumba.is_active == True
                )
                .first()
            )

            if gumba is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Selected Gumba was not found."
                )

            # -----------------------------------------------------
            # IMPORTANT:
            # Existing Gumba must not already have an agent.
            # -----------------------------------------------------

            if gumba.agent_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This Gumba is already assigned to an agent."
                )

            application.gumba_application_type = "EXISTING"
            application.gumba_id = gumba.id

            # Clear previously submitted NEW Gumba information.
            application.new_gumba_name = None
            application.new_gumba_description = None
            application.new_gumba_address = None
            application.new_gumba_district = None
            application.new_gumba_municipality = None
            application.new_gumba_ward_no = None
            application.new_gumba_contact_phone = None
            application.new_gumba_contact_email = None
            application.new_gumba_website = None
            application.new_gumba_latitude = None
            application.new_gumba_longitude = None

        # ---------------------------------------------------------
        # 5. NEW GUMBA
        # ---------------------------------------------------------

        elif (
            application_data.gumba_application_type
            == GumbaApplicationType.NEW
        ):

            if application_data.gumba_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Existing Gumba ID must not be provided when registering a new Gumba."
                )

            # -----------------------------------------------------
            # Check whether a similar Gumba already exists.
            # -----------------------------------------------------

            existing_gumba = (
                db.query(Gumba)
                .filter(
                    Gumba.name == application_data.new_gumba_name,
                    Gumba.district == application_data.new_gumba_district,
                    Gumba.municipality
                    == application_data.new_gumba_municipality,
                    Gumba.ward_no
                    == str(application_data.new_gumba_ward_no),
                    Gumba.is_active == True
                )
                .first()
            )

            if existing_gumba:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="This Gumba is already registered."
                )

            application.gumba_application_type = "NEW"
            application.gumba_id = None

            application.new_gumba_name = (
                application_data.new_gumba_name
            )

            application.new_gumba_description = (
                application_data.new_gumba_description
            )

            application.new_gumba_address = (
                application_data.new_gumba_address
            )

            application.new_gumba_district = (
                application_data.new_gumba_district
            )

            application.new_gumba_municipality = (
                application_data.new_gumba_municipality
            )

            application.new_gumba_ward_no = (
                str(application_data.new_gumba_ward_no)
            )

            application.new_gumba_contact_phone = (
                application_data.new_gumba_contact_phone
            )

            application.new_gumba_contact_email = (
                application_data.new_gumba_contact_email
            )

            application.new_gumba_website = (
                application_data.new_gumba_website
            )

            application.new_gumba_latitude = (
                application_data.new_gumba_latitude
            )

            application.new_gumba_longitude = (
                application_data.new_gumba_longitude
            )

        # ---------------------------------------------------------
        # 6. APPLICANT INFORMATION
        # ---------------------------------------------------------

        application.profile_photo = profile_photo

        application.gender = application_data.gender

        application.address = application_data.address
        application.district = application_data.district
        application.municipality = application_data.municipality
        application.ward_no = str(application_data.ward_no)

        application.designation = application_data.designation

        application.short_bio = application_data.short_bio

        # ---------------------------------------------------------
        # 7. IDENTITY INFORMATION
        # ---------------------------------------------------------

        application.id_type = application_data.id_type
        application.id_number = application_data.id_number

        application.id_document = id_document

        application.gumba_association_letter = (
            gumba_association_letter
        )

        # ---------------------------------------------------------
        # 8. RESET STATUS
        # ---------------------------------------------------------

        application.verification_status = "PENDING"

        # ---------------------------------------------------------
        # 9. SAVE
        # ---------------------------------------------------------

        db.add(application)

        db.commit()

        db.refresh(application)

        return application