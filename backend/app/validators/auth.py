from fastapi import HTTPException

from app.validators.common import (
    is_valid_name,
    is_valid_phone,
    is_valid_password,
)