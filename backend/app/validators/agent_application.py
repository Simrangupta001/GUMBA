from app.validators.common import (
    clean_text,
    is_valid_name,
)
from app.validators.gumba import validate_ward


ALLOWED_GENDERS = {
    "MALE",
    "FEMALE",
    "OTHER",
    "PREFER_NOT_TO_SAY",
}


ALLOWED_ID_TYPES = {
    "CITIZENSHIP",
    "PASSPORT",
    "NATIONAL_ID",
    "DRIVING_LICENSE",
}


def validate_agent_name(value: str) -> str:
    value = value.strip()

    if not is_valid_name(value):
        raise ValueError(
            "Full name must contain valid alphabetic characters "
            "and may contain spaces, hyphens or apostrophes."
        )

    return value


def validate_agent_address(value: str) -> str:
    value = clean_text(value)

    if len(value) < 2:
        raise ValueError(
            "Address must contain at least 2 characters."
        )

    if len(value) > 255:
        raise ValueError(
            "Address cannot exceed 255 characters."
        )

    return value


def validate_designation(value: str) -> str:
    value = clean_text(value)

    if len(value) < 2:
        raise ValueError(
            "Designation must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValueError(
            "Designation cannot exceed 100 characters."
        )

    return value


def validate_short_bio(value: str | None):
    if value is None:
        return None

    value = clean_text(value)

    if len(value) > 2000:
        raise ValueError(
            "Short bio cannot exceed 2000 characters."
        )

    return value


def validate_gender(value: str | None):
    if value is None:
        return None

    value = value.strip().upper()

    if value not in ALLOWED_GENDERS:
        raise ValueError(
            "Invalid gender value."
        )

    return value


def validate_id_type(value: str) -> str:
    value = value.strip().upper()

    if value not in ALLOWED_ID_TYPES:
        raise ValueError(
            "Invalid ID type."
        )

    return value


def validate_id_number(value: str) -> str:
    value = value.strip()

    if len(value) < 3:
        raise ValueError(
            "ID number is too short."
        )

    if len(value) > 100:
        raise ValueError(
            "ID number cannot exceed 100 characters."
        )

    return value