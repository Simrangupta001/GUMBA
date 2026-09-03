from fastapi import UploadFile


MAX_PDF_SIZE = 5 * 1024 * 1024       # 5 MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024     # 5 MB


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


async def validate_pdf(file: UploadFile):
    if not file:
        raise ValueError("PDF document is required.")

    contents = await file.read()

    # Reset file position so it can later be saved
    await file.seek(0)

    if not contents:
        raise ValueError("Uploaded PDF is empty.")

    if len(contents) > MAX_PDF_SIZE:
        raise ValueError(
            "PDF file size cannot exceed 5 MB."
        )

    # PDF magic bytes
    if not contents.startswith(b"%PDF-"):
        raise ValueError(
            "Invalid PDF file."
        )

    return True


async def validate_profile_photo(file: UploadFile):
    if not file:
        raise ValueError(
            "Profile photo is required."
        )

    contents = await file.read()

    await file.seek(0)

    if not contents:
        raise ValueError(
            "Uploaded image is empty."
        )

    if len(contents) > MAX_IMAGE_SIZE:
        raise ValueError(
            "Profile photo cannot exceed 5 MB."
        )

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(
            "Profile photo must be JPG, PNG or WEBP."
        )

    # Basic image signatures
    valid_signature = (
        contents.startswith(b"\xff\xd8\xff") or       # JPEG
        contents.startswith(b"\x89PNG\r\n\x1a\n") or  # PNG
        contents.startswith(b"RIFF")                  # WEBP container
    )

    if not valid_signature:
        raise ValueError(
            "Uploaded file is not a valid image."
        )

    return True