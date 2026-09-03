import re


NAME_REGEX = re.compile(
    r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[ '-][A-Za-zÀ-ÖØ-öø-ÿ]+)*$"
)

USERNAME_REGEX = re.compile(
    r"^[A-Za-z0-9_]{3,30}$"
)

PHONE_REGEX = re.compile(
    r"^[0-9]{10,15}$"
)

PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*\d)"
    r"(?=.*[@$!%*?&])"
    r"[A-Za-z\d@$!%*?&]{8,64}$"
)


def is_valid_name(name: str) -> bool:
    if not isinstance(name, str):
        return False

    name = name.strip()

    if not name:
        return False

    if len(name) < 2 or len(name) > 100:
        return False

    return bool(NAME_REGEX.fullmatch(name))


def is_valid_username(username: str) -> bool:
    if not isinstance(username, str):
        return False

    return bool(USERNAME_REGEX.fullmatch(username))


def is_valid_phone(phone: str) -> bool:
    if not isinstance(phone, str):
        return False

    return bool(PHONE_REGEX.fullmatch(phone))


def is_valid_password(password: str) -> bool:
    if not isinstance(password, str):
        return False

    if len(password) < 8 or len(password) > 64:
        return False

    return bool(PASSWORD_REGEX.fullmatch(password))


def clean_text(value: str) -> str:
    """
    Normalize user-entered text:
    - removes leading/trailing whitespace
    - converts repeated whitespace to a single space
    """
    if not isinstance(value, str):
        return value

    return " ".join(value.strip().split())