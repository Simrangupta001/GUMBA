from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
  )
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import user_required
from app.models.user import User
from app.schemas.agent_application import (
    AgentApplicationCreate,
    AgentApplicationResponse,
)
from app.services.agent_application_service import (
    AgentApplicationService,
)
from app.enums.agent_application import GumbaApplicationType
from fastapi import HTTPException, status

from app.validators.file_upload import (
    read_and_validate_file,
    get_safe_extension,
    IMAGE_MIME_TYPES,
    DOCUMENT_MIME_TYPES,
)

from app.services.file_storage_service import (
    save_file,
    delete_file,
    PROFILE_PHOTO_DIR,
    ID_DOCUMENT_DIR,
    ASSOCIATION_LETTER_DIR,
)

router = APIRouter(
    prefix="/agent-applications",
    tags=["Agent Applications"],
)


@router.post(
    "",
    response_model=AgentApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_agent_application(
    # ---------------------------------------------------------
    # GUMBA APPLICATION
    # ---------------------------------------------------------

    gumba_application_type: GumbaApplicationType = Form(...),

    gumba_id: Optional[int] = Form(None),

    # ---------------------------------------------------------
    # NEW GUMBA INFORMATION
    # ---------------------------------------------------------

    new_gumba_name: Optional[str] = Form(None),

    new_gumba_description: Optional[str] = Form(None),

    new_gumba_address: Optional[str] = Form(None),

    new_gumba_district: Optional[str] = Form(None),

    new_gumba_municipality: Optional[str] = Form(None),

    new_gumba_ward_no: Optional[int] = Form(None),

    new_gumba_contact_phone: Optional[str] = Form(None),

    new_gumba_contact_email: Optional[str] = Form(None),

    new_gumba_website: Optional[str] = Form(None),

    new_gumba_latitude: Optional[float] = Form(None),

    new_gumba_longitude: Optional[float] = Form(None),

    # ---------------------------------------------------------
    # APPLICANT PROFILE
    # ---------------------------------------------------------

    gender: Optional[str] = Form(None),

    address: str = Form(...),

    district: str = Form(...),

    municipality: str = Form(...),

    ward_no: int = Form(...),

    designation: str = Form(...),

    short_bio: Optional[str] = Form(None),

    # ---------------------------------------------------------
    # IDENTITY
    # ---------------------------------------------------------

    id_type: str = Form(...),

    id_number: str = Form(...),

    # ---------------------------------------------------------
    # FILES
    # ---------------------------------------------------------

    profile_photo: Optional[UploadFile] = File(None),

    id_document: UploadFile = File(...),

    gumba_association_letter: UploadFile = File(...),

    # ---------------------------------------------------------
    # DEPENDENCIES
    # ---------------------------------------------------------

    db: Session = Depends(get_db),

    current_user: User = Depends(user_required),
):
    # ---------------------------------------------------------
    # BUILD APPLICATION DATA
    # ---------------------------------------------------------

    application_data = AgentApplicationCreate(
        gumba_application_type=gumba_application_type,

        gumba_id=gumba_id,

        new_gumba_name=new_gumba_name,
        new_gumba_description=new_gumba_description,
        new_gumba_address=new_gumba_address,
        new_gumba_district=new_gumba_district,
        new_gumba_municipality=new_gumba_municipality,
        new_gumba_ward_no=new_gumba_ward_no,
        new_gumba_contact_phone=new_gumba_contact_phone,
        new_gumba_contact_email=new_gumba_contact_email,
        new_gumba_website=new_gumba_website,
        new_gumba_latitude=new_gumba_latitude,
        new_gumba_longitude=new_gumba_longitude,

        gender=gender,

        address=address,
        district=district,
        municipality=municipality,
        ward_no=ward_no,

        designation=designation,

        short_bio=short_bio,

        id_type=id_type,
        id_number=id_number,
    )

    # ---------------------------------------------------------
    # SERVICE
    # ---------------------------------------------------------
    stored_profile_photo = None
    stored_id_document = None
    stored_association_letter = None

    try:

        # -------------------------------------------------
        # 3. Validate + save profile photo
        # -------------------------------------------------

        if profile_photo:
            content, detected_type = await read_and_validate_file(
                profile_photo,
                IMAGE_MIME_TYPES,
            )

            stored_profile_photo = save_file(
                content=content,
                directory=PROFILE_PHOTO_DIR,
                extension=get_safe_extension(detected_type),
            )

        # -------------------------------------------------
        # 4. Validate + save ID document
        # -------------------------------------------------

        content, detected_type = await read_and_validate_file(
            id_document,
            DOCUMENT_MIME_TYPES,
        )

        stored_id_document = save_file(
            content=content,
            directory=ID_DOCUMENT_DIR,
            extension=get_safe_extension(detected_type),
        )

        # -------------------------------------------------
        # 5. Validate + save Gumba association letter
        # -------------------------------------------------

        content, detected_type = await read_and_validate_file(
            gumba_association_letter,
            DOCUMENT_MIME_TYPES,
        )

        stored_association_letter = save_file(
            content=content,
            directory=ASSOCIATION_LETTER_DIR,
            extension=get_safe_extension(detected_type),
        )

        # -------------------------------------------------
        # 6. Save application in database
        # -------------------------------------------------

        return AgentApplicationService.create_application(
            db=db,
            current_user=current_user,
            application_data=application_data,
            profile_photo=stored_profile_photo,
            id_document=stored_id_document,
            gumba_association_letter=stored_association_letter,
        )

    except Exception:

        # -------------------------------------------------
        # 7. Cleanup files if anything fails
        # -------------------------------------------------

        delete_file(stored_profile_photo)
        delete_file(stored_id_document)
        delete_file(stored_association_letter)

        raise