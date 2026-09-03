from pathlib import Path
from uuid import uuid4


UPLOAD_ROOT = Path("uploads")

PROFILE_PHOTO_DIR = UPLOAD_ROOT / "profile_photos"
ID_DOCUMENT_DIR = UPLOAD_ROOT / "id_documents"
ASSOCIATION_LETTER_DIR = UPLOAD_ROOT / "association_letters"


class FileStorageService:

    @staticmethod
    def save(
        content: bytes,
        directory: Path,
        extension: str
    ) -> str:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = f"{uuid4().hex}{extension}"

        file_path = directory / filename

        try:
            file_path.write_bytes(content)

        except Exception:
            raise RuntimeError(
                "Unable to process the uploaded file."
            )

        return str(file_path)