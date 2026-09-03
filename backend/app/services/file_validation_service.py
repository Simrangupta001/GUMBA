from fastapi import UploadFile, HTTPException, status
from io import BytesIO

from PIL import Image


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
}

DOCUMENT_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
}


async def validate_upload(
    file: UploadFile,
    allowed_types: set[str],
    field_name: str
) -> bytes:

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} is required."
        )

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"Unsupported {field_name} format."
            )
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"{field_name} cannot be empty."
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"{field_name} must not exceed 5 MB."
        )

    return content

def validate_real_image(
    content: bytes,
    field_name: str
):
    try:
        image = Image.open(BytesIO(content))
        image.verify()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"The uploaded {field_name} "
                "is not a valid JPEG or PNG image."
            )
        )

def validate_profile_photo(
    content: bytes,
    mime_type: str
):
    if mime_type not in IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                "Unsupported profile photo format. "
                "Only JPEG and PNG images are allowed."
            )
        )

    validate_real_image(
        content,
        "profile photo"
    )