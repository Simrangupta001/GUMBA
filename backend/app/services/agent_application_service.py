from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.config import settings
from app.models.agent_application import AgentApplication
from app.models.gumba import Gumba
from app.models.user import User
from app.schemas.agent_application import AgentApplicationCreate
from app.enums.agent_application import GumbaApplicationType
from app.services.agent_service import get_agent_role
from app.services.email_service import EmailService

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

    # ---------------------------------------------------------
    # ADMIN REVIEW
    # ---------------------------------------------------------

    @staticmethod
    def _get_application_with_relations(
        db: Session,
        application_id: int,
    ):
        application = (
            db.query(AgentApplication)
            .options(
                joinedload(AgentApplication.user),
                joinedload(AgentApplication.gumba),
            )
            .filter(AgentApplication.id == application_id)
            .first()
        )

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent application not found."
            )

        return application

    @staticmethod
    def get_all_applications(
        db: Session,
        verification_status: str | None = None,
    ):
        query = db.query(AgentApplication).options(
            joinedload(AgentApplication.user),
            joinedload(AgentApplication.gumba),
        )

        if verification_status is not None:
            query = query.filter(
                AgentApplication.verification_status
                == verification_status.upper()
            )

        return query.order_by(AgentApplication.created_at.desc()).all()

    @staticmethod
    def get_application_by_id(
        db: Session,
        application_id: int,
    ):
        return AgentApplicationService._get_application_with_relations(
            db, application_id
        )

    @staticmethod
    def approve_application(
        db: Session,
        application_id: int,
    ):
        # -----------------------------------------------------
        # Lock the application row for the duration of this
        # transaction so two admins approving the same
        # application at the same time can't both proceed
        # (the second one blocks here until the first commits,
        # then sees PENDING is no longer true and gets a 409).
        # -----------------------------------------------------

        application = (
            db.query(AgentApplication)
            .filter(AgentApplication.id == application_id)
            .with_for_update()
            .first()
        )

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent application not found."
            )

        if application.verification_status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "This application is already "
                    f"{application.verification_status.lower()}."
                )
            )

        applicant = (
            db.query(User)
            .filter(User.id == application.user_id)
            .first()
        )

        if applicant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant no longer exists."
            )

        if applicant.role.name != "USER":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Applicant no longer holds the USER role."
            )

        # -------------------------------------------------
        # EXISTING GUMBA
        # -------------------------------------------------

        if application.gumba_application_type == "EXISTING":

            gumba = (
                db.query(Gumba)
                .filter(Gumba.id == application.gumba_id)
                .with_for_update()
                .first()
            )

            if gumba is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Selected Gumba no longer exists."
                )

            if not gumba.is_active:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Selected Gumba is no longer active."
                )

            if gumba.agent_id is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "Selected Gumba has already been "
                        "assigned to an agent."
                    )
                )

            gumba.agent_id = applicant.id

        # -------------------------------------------------
        # NEW GUMBA
        # -------------------------------------------------

        elif application.gumba_application_type == "NEW":

            duplicate_gumba = (
                db.query(Gumba)
                .filter(
                    Gumba.name == application.new_gumba_name,
                    Gumba.district == application.new_gumba_district,
                    Gumba.municipality
                    == application.new_gumba_municipality,
                    Gumba.ward_no == application.new_gumba_ward_no,
                    Gumba.is_active == True,
                )
                .first()
            )

            if duplicate_gumba:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "A Gumba matching this application's "
                        "details has already been registered."
                    )
                )

            gumba = Gumba(
                name=application.new_gumba_name,
                description=application.new_gumba_description,
                address=application.new_gumba_address,
                district=application.new_gumba_district,
                municipality=application.new_gumba_municipality,
                ward_no=application.new_gumba_ward_no,
                contact_phone=application.new_gumba_contact_phone,
                contact_email=application.new_gumba_contact_email,
                website=application.new_gumba_website,
                latitude=application.new_gumba_latitude,
                longitude=application.new_gumba_longitude,
                agent_id=applicant.id,
            )

            db.add(gumba)

            # Assign gumba.id without ending the transaction, so
            # everything below still commits together atomically.
            db.flush()

            application.gumba_id = gumba.id

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown Gumba application type."
            )

        # -------------------------------------------------
        # PROMOTE APPLICANT -> AGENT
        # (reuses the same role lookup used when an admin
        # creates an agent directly via /admin/agents)
        # -------------------------------------------------

        agent_role = get_agent_role(db)
        applicant.role_id = agent_role.id

        application.verification_status = "APPROVED"

        db.commit()
        AgentApplicationService._notify_application_status_change(
            db, application, applicant
        )

        return AgentApplicationService._get_application_with_relations(
            db, application.id
        )

    @staticmethod
    def reject_application(
        db: Session,
        application_id: int,
    ):
        application = (
            db.query(AgentApplication)
            .filter(AgentApplication.id == application_id)
            .with_for_update()
            .first()
        )

        if application is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent application not found."
            )

        if application.verification_status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "This application is already "
                    f"{application.verification_status.lower()}."
                )
            )

        # User stays USER; the application record itself is kept
        # (not deleted) so it can be reused on their next
        # submission - matches create_application()'s existing
        # REJECTED-row reuse behavior.
        application.verification_status = "REJECTED"

        db.commit()
        AgentApplicationService._notify_application_status_change(
            db, application
        )

        return AgentApplicationService._get_application_with_relations(
            db, application.id
        )
    # ---------------------------------------------------------
    # EMAIL NOTIFICATIONS
    # ---------------------------------------------------------

    @staticmethod
    def _notify_application_status_change(
        db: Session,
        application: "AgentApplication",
        applicant: "User | None" = None,
    ):
        if applicant is None:
            applicant = (
                db.query(User)
                .filter(User.id == application.user_id)
                .first()
            )

        status_label = (
            "Approved"
            if application.verification_status == "APPROVED"
            else "Rejected"
        )

        # For an APPROVED application, gumba_id always points at a
        # real Gumba by this point (either the existing one, or the
        # one just created for a NEW application). For a REJECTED
        # NEW-gumba application, no Gumba was ever created, so fall
        # back to the name the applicant originally typed in.
        if application.gumba_id:
            gumba = (
                db.query(Gumba)
                .filter(Gumba.id == application.gumba_id)
                .first()
            )
            gumba_name = gumba.name if gumba else "N/A"
        else:
            gumba_name = application.new_gumba_name or "N/A"

        applicant_name = applicant.full_name if applicant else "Unknown"
        banner_color = (
            "#16a34a"
            if application.verification_status == "APPROVED"
            else "#dc2626"
        )

        # ---- Applicant email ----

        if applicant and applicant.email:
            EmailService.send_templated_email(
                to=applicant.email,
                subject=(
                    f"Your agent application has been "
                    f"{status_label.lower()}"
                ),
                template_name="agent_application_status.html",
                context={
                    "status": application.verification_status,
                    "status_label": status_label,
                    "greeting_name": applicant_name,
                    "is_super_admin_copy": False,
                    "application_id": application.id,
                    "applicant_name": applicant_name,
                    "gumba_name": gumba_name,
                    "gumba_type": application.gumba_application_type,
                    "designation": application.designation,
                    "banner_color": banner_color,
                },
            )

        # ---- Super Admin email ----
        # Fixed recipient from .env (settings.SUPER_ADMIN_EMAIL), per
        # explicit decision - not a dynamic "all SUPER_ADMIN-role
        # users" lookup.

        if settings.SUPER_ADMIN_EMAIL:
            EmailService.send_templated_email(
                to=settings.SUPER_ADMIN_EMAIL,
                subject=(
                    f"Agent application #{application.id} has been "
                    f"{status_label.lower()}"
                ),
                template_name="agent_application_status.html",
                context={
                    "status": application.verification_status,
                    "status_label": status_label,
                    "greeting_name": "Super Admin",
                    "is_super_admin_copy": True,
                    "application_id": application.id,
                    "applicant_name": applicant_name,
                    "gumba_name": gumba_name,
                    "gumba_type": application.gumba_application_type,
                    "designation": application.designation,
                    "banner_color": banner_color,
                },
            )