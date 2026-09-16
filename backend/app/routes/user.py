from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import user_required, get_current_user
from app.models.user import User
from app.schemas.user import UserProfileResponse, UserProfileUpdate
from app.validators.file_upload import (
    read_and_validate_file,
    get_safe_extension,
    IMAGE_MIME_TYPES,
)
from app.services.file_storage_service import (
    save_file,
    delete_file,
    USER_PROFILE_PHOTO_DIR,
)

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(user_required)
):
    return {
        "message": "Welcome User Dashboard",
        "user": current_user.full_name
    }


def _build_profile_response(current_user: User) -> UserProfileResponse:
    return UserProfileResponse(
        id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone,
        role=current_user.role.name,
        profile_photo=current_user.profile_photo,
        address=current_user.address,
        district=current_user.district,
        municipality=current_user.municipality,
        ward_no=current_user.ward_no,
        is_active=current_user.is_active,
    )


@router.get(
    "/profile",
    response_model=UserProfileResponse,
)
def get_profile(
    # Any authenticated user (USER, AGENT, ADMIN, SUPER_ADMIN) can
    # view/edit their own profile - this isn't donor-specific, so
    # get_current_user is used here rather than user_required.
    current_user: User = Depends(get_current_user),
):
    return _build_profile_response(current_user)


@router.patch(
    "/profile",
    response_model=UserProfileResponse,
)
def update_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    JSON body. A field left OUT of the request body is left
    untouched; a field explicitly sent as null clears it.
    """
    provided_fields = payload.model_dump(exclude_unset=True)

    for field_name in (
        "address", "district", "municipality", "ward_no"
    ):
        if field_name in provided_fields:
            setattr(current_user, field_name, getattr(payload, field_name))

    db.commit()
    db.refresh(current_user)

    return _build_profile_response(current_user)


@router.patch(
    "/profile/photo",
    response_model=UserProfileResponse,
)
async def update_profile_photo(
    profile_photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_photo = current_user.profile_photo

    content, detected_type = await read_and_validate_file(
        profile_photo,
        IMAGE_MIME_TYPES,
    )

    new_photo_path = save_file(
        content=content,
        directory=USER_PROFILE_PHOTO_DIR,
        extension=get_safe_extension(detected_type),
    )

    current_user.profile_photo = new_photo_path

    db.commit()
    db.refresh(current_user)

    if old_photo and old_photo != new_photo_path:
        delete_file(old_photo)

    return _build_profile_response(current_user)


@router.delete(
    "/profile/photo",
    response_model=UserProfileResponse,
)
def remove_profile_photo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    old_photo = current_user.profile_photo
    current_user.profile_photo = None

    db.commit()
    db.refresh(current_user)

    if old_photo:
        delete_file(old_photo)

    return _build_profile_response(current_user)