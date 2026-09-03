import re

from app.validators.common import (
    is_valid_name,
    is_valid_phone,
    is_valid_password,
)
from app.validators.gumba import validate_ward


def validate_agent_name(value: str) -> str:
    if value is None:
        raise ValueError("Full name is required.")

    value = value.strip()

    if not value:
        raise ValueError("Full name cannot be empty.")

    if not is_valid_name(value):
        raise ValueError(
            "Full name must contain only alphabets and spaces."
        )

    if len(value) < 2:
        raise ValueError(
            "Full name must contain at least 2 characters."
        )

    return value


def validate_agent_phone(value: str) -> str:
    if value is None:
        raise ValueError("Phone number is required.")

    value = value.strip()

    if not is_valid_phone(value):
        raise ValueError(
            "Phone number must contain 10 to 15 digits."
        )

    return value


def validate_agent_address(value: str) -> str:
    if value is None:
        raise ValueError("Address is required.")

    value = value.strip()

    if not value:
        raise ValueError("Address cannot be empty.")

    if len(value) < 2:
        raise ValueError(
            "Address must contain at least 2 characters."
        )

    if len(value) > 255:
        raise ValueError(
            "Address cannot exceed 255 characters."
        )

    return value


def validate_agent_location(value: str, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required.")

    value = value.strip()

    if not value:
        raise ValueError(
            f"{field_name} cannot be empty."
        )

    if len(value) < 2:
        raise ValueError(
            f"{field_name} must contain at least 2 characters."
        )

    if not re.fullmatch(r"[A-Za-z .'-]+", value):
        raise ValueError(
            f"{field_name} contains invalid characters."
        )

    return value


def validate_designation(value: str) -> str:
    if value is None:
        raise ValueError("Designation is required.")

    value = value.strip()

    if not value:
        raise ValueError(
            "Designation cannot be empty."
        )

    if len(value) < 2:
        raise ValueError(
            "Designation must contain at least 2 characters."
        )

    if len(value) > 100:
        raise ValueError(
            "Designation cannot exceed 100 characters."
        )

    return value


def validate_bio(value: str) -> str:
    if value is None:
        return value

    value = value.strip()

    if len(value) > 1000:
        raise ValueError(
            "Bio cannot exceed 1000 characters."
        )

    return value


def validate_id_type(value: str) -> str:
    allowed_types = {
        "CITIZENSHIP",
        "PASSPORT",
        "NATIONAL_ID",
        "DRIVING_LICENSE",
    }

    if value is None:
        raise ValueError("ID type is required.")

    value = value.strip().upper()

    if value not in allowed_types:
        raise ValueError(
            "Invalid ID type."
        )

    return value


def validate_id_number(value: str) -> str:
    if value is None:
        raise ValueError("ID number is required.")

    value = value.strip()

    if not value:
        raise ValueError(
            "ID number cannot be empty."
        )

    if len(value) < 3:
        raise ValueError(
            "ID number is too short."
        )

    if len(value) > 50:
        raise ValueError(
            "ID number cannot exceed 50 characters."
        )

    if not re.fullmatch(r"[A-Za-z0-9./\- ]+", value):
        raise ValueError(
            "ID number contains invalid characters."
        )

    return value