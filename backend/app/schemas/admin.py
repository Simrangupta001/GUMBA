from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from pydantic import  ConfigDict
from typing import Optional
from pydantic import BaseModel, EmailStr


class AdminCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str
    password: str = Field(min_length=8)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        value = value.strip()

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError("Name must contain only alphabets and spaces.")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"[0-9]{10,15}", value):
            raise ValueError("Phone must contain 10 to 15 digits.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one number.")

        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("Password must contain at least one special character.")

        return value

class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)

class AdminUpdate(BaseModel):
        full_name: Optional[str] = Field(
            default=None,
            min_length=2,
            max_length=100
        )
        email: Optional[EmailStr] = None
        phone: Optional[str] = None
        password: Optional[str] = Field(
            default=None,
            min_length=8
        )
        is_active: Optional[bool] = None

        @field_validator("full_name")
        @classmethod
        def validate_full_name(cls, value):
            if value is None:
                return value

            value = value.strip()

            if not re.fullmatch(r"[A-Za-z ]+", value):
                raise ValueError(
                    "Name must contain only alphabets and spaces."
                )

            return value

        @field_validator("phone")
        @classmethod
        def validate_phone(cls, value):
            if value is None:
                return value

            if not re.fullmatch(r"[0-9]{10,15}", value):
                raise ValueError(
                    "Phone must contain 10 to 15 digits."
                )

            return value

        @field_validator("password")
        @classmethod
        def validate_password(cls, value):
            if value is None:
                return value

            if not re.search(r"[A-Z]", value):
                raise ValueError(
                    "Password must contain at least one uppercase letter."
                )

            if not re.search(r"[a-z]", value):
                raise ValueError(
                    "Password must contain at least one lowercase letter."
                )

            if not re.search(r"[0-9]", value):
                raise ValueError(
                    "Password must contain at least one number."
                )

            if not re.search(r"[@$!%*?&]", value):
                raise ValueError(
                    "Password must contain at least one special character."
                )

            return value

class AdminStatusUpdate(BaseModel):
    is_active: bool

