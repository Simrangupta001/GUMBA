import re


def validate_gumba_phone(phone: str) -> str:
    """
    Validate Nepali mobile and landline/telephone numbers.

    Accepted examples:
        9841234567
        9812345678
        01-4567890
        01 4567890
        +977-9841234567
        +977-1-4567890
    """

    if not phone:
        raise ValueError("Phone number cannot be empty.")

    cleaned = re.sub(r"[\s\-()]", "", phone)

    if cleaned.startswith("+977"):
        cleaned = cleaned[4:]

    if not cleaned.isdigit():
        raise ValueError(
            "Phone number must contain only valid digits and formatting."
        )

    # Remove Nepal's national trunk prefix
    if cleaned.startswith("0"):
        number = cleaned[1:]
    else:
        number = cleaned

    # Mobile
    if re.fullmatch(r"(96|97|98)\d{8}", number):
        return phone.strip()

    # Landline
    if re.fullmatch(r"[1-9]\d{7,8}", number):
        return phone.strip()

    raise ValueError(
        "Enter a valid Nepali mobile or telephone number."
    )


def validate_ward(value: str) -> str:
    """
    Validate municipality ward number.

    Examples:
        1
        5
        11
        32
    """

    if value is None:
        return value

    value = str(value).strip()

    if not value:
        raise ValueError("Ward number cannot be empty.")

    if not re.fullmatch(r"\d{1,2}", value):
        raise ValueError(
            "Ward number must contain 1 or 2 digits."
        )

    ward = int(value)

    if ward < 1 or ward > 99:
        raise ValueError(
            "Ward number must be between 1 and 99."
        )

    return value

def is_valid_gumba_phone(phone: str) -> bool:
    """
    Validate Gumba contact phone number.

    Accepts:
    - 10 to 15 digits
    """
    return bool(re.fullmatch(r"[0-9]{10,15}", phone))