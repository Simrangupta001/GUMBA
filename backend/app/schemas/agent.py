from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from app.validators.agent import (
    validate_agent_name,
    validate_agent_phone,
    validate_agent_address,
    validate_agent_location,
    validate_designation,
    validate_bio,
    validate_id_type,
    validate_id_number,
)
from app.validators.gumba import validate_ward


class AgentCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    password: str = Field(..., min_length=6)


class AgentUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)


class AgentResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


class AgentStatusUpdate(BaseModel):
    is_active: bool

class AgentApplicationCreate(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str

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
        max_length=2
    )

    designation: str = Field(
        min_length=2,
        max_length=100
    )

    bio: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    id_type: str

    id_number: str

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        return validate_agent_name(value)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        return validate_agent_phone(value)

    @field_validator("address")
    @classmethod
    def validate_address(cls, value):
        return validate_agent_address(value)

    @field_validator("district")
    @classmethod
    def validate_district(cls, value):
        return validate_agent_location(
            value,
            "District"
        )

    @field_validator("municipality")
    @classmethod
    def validate_municipality(cls, value):
        return validate_agent_location(
            value,
            "Municipality"
        )

    @field_validator("ward_no")
    @classmethod
    def validate_ward_number(cls, value):
        return validate_ward(value)

    @field_validator("designation")
    @classmethod
    def validate_designation_field(cls, value):
        return validate_designation(value)

    @field_validator("bio")
    @classmethod
    def validate_bio_field(cls, value):
        return validate_bio(value)

    @field_validator("id_type")
    @classmethod
    def validate_id_type_field(cls, value):
        return validate_id_type(value)

    @field_validator("id_number")
    @classmethod
    def validate_id_number_field(cls, value):
        return validate_id_number(value)