from typing import Optional
import re

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class AgentApplicationCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str

    profile_photo: Optional[str] = None

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    address: str = Field(
        min_length=2,
        max_length=255
    )

    district: str = Field(
        min_length=2,
        max_length=100
    )

    municipality: str = Field(
        min_length=2,
        max_length=100
    )

    ward_no: str = Field(
        min_length=1,
        max_length=20
    )

    designation: str = Field(
        min_length=2,
        max_length=100
    )

    short_bio: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    id_type: str = Field(
        min_length=2,
        max_length=50
    )

    id_number: str = Field(
        min_length=2,
        max_length=100
    )

    id_document: str

    gumba_association_letter: str


    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        value = value.strip()

        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise ValueError(
                "Name must contain only alphabets and spaces."
            )

        return value


    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"[0-9]{10,15}", value):
            raise ValueError(
                "Phone must contain 10 to 15 digits."
            )

        return value


    @field_validator(
        "address",
        "district",
        "municipality",
        "designation",
        "id_type",
        "id_number"
    )
    @classmethod
    def validate_text_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty."
            )

        return value


class AgentApplicationResponse(BaseModel):

    id: int
    user_id: int

    full_name: str
    email: EmailStr
    phone: str

    profile_photo: Optional[str]
    gender: Optional[str]

    address: str
    district: str
    municipality: str
    ward_no: str

    designation: str
    short_bio: Optional[str]

    id_type: str

    # Don't expose sensitive verification documents
    verification_status: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )