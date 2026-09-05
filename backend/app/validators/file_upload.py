from io import BytesIO

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader


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


def validate_file_size(file_content: bytes) -> None:
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File must not exceed 5 MB."
        )


def detect_file_type(file_content: bytes) -> str:
    """
    Detect the actual file type from its binary signature.

    This does NOT trust the MIME type supplied by the client.
    """

    # JPEG
    if file_content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"

    # PNG
    if file_content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"

    # PDF
    if file_content.startswith(b"%PDF-"):
        return "application/pdf"

    return "application/octet-stream"


def validate_image(file_content: bytes, detected_type: str) -> None:
    """
    Validate that the file is an actual readable image,
    not merely a file with an image extension/signature.
    """

    if detected_type not in IMAGE_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG and PNG images are allowed."
        )

    try:
        with Image.open(BytesIO(file_content)) as image:
            image.verify()

        # Re-open after verify() because verify() invalidates
        # the image object for normal reading.
        with Image.open(BytesIO(file_content)) as image:
            image.load()

    except (UnidentifiedImageError, OSError, SyntaxError):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The uploaded image is invalid or corrupted."
        )


def validate_pdf(file_content: bytes) -> None:
    """
    Validate that the file is a readable PDF.
    """

    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The uploaded PDF is invalid or corrupted."
        )

    try:
        PdfReader(BytesIO(file_content))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="The uploaded PDF is invalid or corrupted."
        )


async def read_and_validate_file(
    file: UploadFile,
    allowed_mime_types: set[str],
) -> bytes:

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is required."
        )

    # ---------------------------------------------------------
    # 1. Read file
    # ---------------------------------------------------------

    content = await file.read()

    # ---------------------------------------------------------
    # 2. Size validation
    # ---------------------------------------------------------

    validate_file_size(content)

    # ---------------------------------------------------------
    # 3. Detect actual file type
    # ---------------------------------------------------------

    detected_type = detect_file_type(content)

    # ---------------------------------------------------------
    # 4. Check actual type against allowed types
    # ---------------------------------------------------------

    if detected_type not in allowed_mime_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type."
        )

    # ---------------------------------------------------------
    # 5. Validate actual file contents
    # ---------------------------------------------------------

    if detected_type in IMAGE_MIME_TYPES:

        validate_image(
            content,
            detected_type
        )

    elif detected_type == "application/pdf":

        validate_pdf(content)

    return content

def get_safe_extension(mime_type: str) -> str:

    extensions = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
    }

    extension = extensions.get(mime_type)

    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type."
        )

    return extension