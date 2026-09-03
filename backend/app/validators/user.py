from app.validators.common import (
    is_valid_name,
    is_valid_phone,
    is_valid_password,
)


def validate_full_name(name: str) -> str:
    name = name.strip()

    if not is_valid_name(name):
        raise ValueError(
            "Name must contain valid alphabetic characters "
            "and may contain spaces, hyphens or apostrophes."
        )

    return name


def validate_phone(phone: str) -> str:
    phone = phone.strip()

    if not is_valid_phone(phone):
        raise ValueError(
            "Phone number must contain 10 to 15 digits."
        )

    return phone


def validate_password(password: str) -> str:
    if not is_valid_password(password):
        raise ValueError(
            "Password must be 8-64 characters and contain "
            "uppercase, lowercase, number and special character."
        )

    return password