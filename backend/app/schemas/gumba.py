from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
import re
from app.validators.gumba import is_valid_gumba_phone

class GumbaCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000
    )

    address: str = Field(
        min_length=2,
        max_length=255
    )

    district: str = Field(
        min_length=2,
        max_length=100
    )

    municipality: Optional[str] = Field(
        default=None,
        max_length=100
    )

    ward_no: Optional[str] = Field(
        default=None,
        max_length=20
    )

    contact_phone: Optional[str] = None

    contact_email: Optional[EmailStr] = None

    website: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    photos: Optional[list[str]] = None

    videos: Optional[list[str]] = None

    agent_id: Optional[int] = None

    @field_validator(
        "name",
        "address",
        "district",
        "municipality"
    )
    @classmethod
    def validate_text(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty.")

        return value

    @field_validator("contact_phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not is_valid_gumba_phone(value):
            raise ValueError(
                "Enter a valid mobile or telephone number."
            )

        return value

class GumbaAgentResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]

    model_config = ConfigDict(
        from_attributes=True
    )
    
class GumbaResponse(BaseModel):

    id: int
    name: str
    description: Optional[str]
    address: str
    district: str
    municipality: Optional[str]
    ward_no: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    website: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    photos: Optional[list[str]]
    videos: Optional[list[str]]
    agent_id: Optional[int]
    agent: Optional[GumbaAgentResponse]
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )



