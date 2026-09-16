from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=100)

class UserProfileResponse(BaseModel):
    """
    Full profile for the logged-in user, regardless of role - not
    donation-scoped. Built manually in the route (not from_attributes
    off the ORM object directly), same as the existing /auth/me
    endpoint already does, because `role` is a relationship object
    on the model and needs to become a plain string here.
    """

    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str]
    role: str

    profile_photo: Optional[str]
    address: Optional[str]
    district: Optional[str]
    municipality: Optional[str]
    ward_no: Optional[str]

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class UserProfileUpdate(BaseModel):
    """
    JSON body (not multipart Form) - deliberately, so real PATCH
    semantics work: a field left out of the JSON entirely is left
    untouched, and a field explicitly sent as null clears it.
    """

    address: Optional[str] = Field(default=None, max_length=255)
    district: Optional[str] = Field(default=None, max_length=100)
    municipality: Optional[str] = Field(default=None, max_length=100)
    ward_no: Optional[str] = Field(default=None, max_length=20)

    @field_validator(
        "address", "district", "municipality", "ward_no"
    )
    @classmethod
    def normalize(cls, value):
        if value is None:
            return value

        value = value.strip()

        return value or None