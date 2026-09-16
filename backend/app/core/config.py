from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )

    # -------------------------------------------------
    # EMAIL
    # -------------------------------------------------
    MAIL_HOST = os.getenv("MAIL_HOST")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_FROM = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "GUMBA")

    # If MAIL_HOST is not configured (e.g. local dev without SMTP
    # credentials), EmailService logs instead of sending, so the
    # rest of the app keeps working without email set up.
    MAIL_ENABLED = bool(MAIL_HOST and MAIL_USERNAME and MAIL_PASSWORD)

    # Fixed notification recipients (not tied to a specific DB user -
    # simplest option per current requirements; can be swapped for a
    # dynamic "all users with this role" query later without callers
    # changing, since they only ever reference settings.ADMIN_EMAIL /
    # settings.SUPER_ADMIN_EMAIL).
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    SUPER_ADMIN_EMAIL = os.getenv("SUPER_ADMIN_EMAIL")

    # -------------------------------------------------
    # PASSWORD RESET
    # -------------------------------------------------
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 30)
    )

    # Optional: if you have a frontend, set this to its reset-password
    # page (e.g. https://gumba.org/reset-password) and the email will
    # include a clickable link with ?token=... appended. If unset,
    # the email just shows the raw token for manual/API use.
    FRONTEND_RESET_PASSWORD_URL = os.getenv(
        "FRONTEND_RESET_PASSWORD_URL", ""
    )


settings = Settings()






