from fastapi import HTTPException, status

from app.validators.common import (
    is_valid_name,
    is_valid_phone,
    is_valid_password,
)


def validate_registration_data(
    full_name: str,
    phone: str,
    password: str,
):
    errors = {}

    if not is_valid_name(full_name):
        errors["full_name"] = (
            "Name must contain valid alphabetic characters "
            "and may contain spaces, hyphens or apostrophes."
        )

    if not is_valid_phone(phone):
        errors["phone"] = (
            "Phone number must contain 10 to 15 digits."
        )

    if not is_valid_password(password):
        errors["password"] = (
            "Password must be 8-64 characters and contain "
            "uppercase, lowercase, number and special character."
        )

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
        )