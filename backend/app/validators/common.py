import re


NAME_REGEX = r"^[A-Za-z ]+$"

USERNAME_REGEX = r"^[A-Za-z0-9_]+$"

PHONE_REGEX = r"^[0-9]{10,15}$"

PASSWORD_REGEX = (
    r"^(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*\d)"
    r"(?=.*[@$!%*?&])"
    r"[A-Za-z\d@$!%*?&]{8,}$"
)


def is_valid_name(name: str):
    return re.fullmatch(NAME_REGEX, name)


def is_valid_username(username: str):
    return re.fullmatch(USERNAME_REGEX, username)


def is_valid_phone(phone: str):
    return re.fullmatch(PHONE_REGEX, phone)


def is_valid_password(password: str):
    return re.fullmatch(PASSWORD_REGEX, password)