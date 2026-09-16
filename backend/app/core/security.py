import bcrypt
import hashlib
from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def password_fingerprint(password_hash: str) -> str:
    """
    A short, non-reversible fingerprint of a user's CURRENT password
    hash. Embedding this in a password-reset token gives "single use"
    behavior without needing a database table of issued/used tokens:
    once the password actually changes, the fingerprint baked into
    any previously issued reset token no longer matches, so that
    token is rejected even if it hasn't expired yet.
    """
    return hashlib.sha256(password_hash.encode()).hexdigest()[:16]


def create_password_reset_token(user) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "scope": "password_reset",
        "pwd_fp": password_fingerprint(user.password),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_password_reset_token(token: str) -> dict:
    """
    Decodes and validates a password-reset token's signature,
    expiry, and scope. Raises jose.JWTError (same exception family
    already used by get_current_user) on any failure - callers
    should catch JWTError and turn it into a 400.

    Does NOT check the password fingerprint against the current
    user - that requires a DB lookup, so it's the caller's
    responsibility once it has fetched the user.
    """
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

    if payload.get("scope") != "password_reset":
        from jose import JWTError
        raise JWTError("Invalid token scope.")

    return payload