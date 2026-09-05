from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, status

UPLOAD_ROOT = Path("uploads")

AGENT_APPLICATION_ROOT = (
    UPLOAD_ROOT / "agent_applications"
)

PROFILE_PHOTO_DIR = (
    AGENT_APPLICATION_ROOT / "profile_photos"
)

ID_DOCUMENT_DIR = (
    AGENT_APPLICATION_ROOT / "id_documents"
)

ASSOCIATION_LETTER_DIR = (
    AGENT_APPLICATION_ROOT / "association_letters"
)

def initialize_storage() -> None:

    PROFILE_PHOTO_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ID_DOCUMENT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ASSOCIATION_LETTER_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def save_file(
    content: bytes,
    directory: Path,
    extension: str,
) -> str:

    initialize_storage()

    filename = f"{uuid4().hex}{extension}"

    file_path = directory / filename

    try:

        file_path.write_bytes(content)

    except OSError:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to store uploaded file."
        )

    # Return application-relative reference,
    # not an absolute server filesystem path.
    return str(file_path)


def delete_file(file_reference: str | None) -> None:

    if not file_reference:
        return

    try:

        path = Path(file_reference)

        if path.exists() and path.is_file():
            path.unlink()

    except OSError:
        # Do not expose filesystem details to the client.
        pass

    


#
#
# class FileStorageService:
#
#     @staticmethod
#     def save(
#         content: bytes,
#         directory: Path,
#         extension: str
#     ) -> str:
#
#         directory.mkdir(
#             parents=True,
#             exist_ok=True
#         )
#
#         filename = f"{uuid4().hex}{extension}"
#
#         file_path = directory / filename
#
#         try:
#             file_path.write_bytes(content)
#
#         except Exception:
#             raise RuntimeError(
#                 "Unable to process the uploaded file."
#             )
#
#         return str(file_path)