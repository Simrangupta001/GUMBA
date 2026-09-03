from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional


class DonationCreate(BaseModel):

    gumba_id: int = Field(gt=0)

    amount: float = Field(
        gt=0,
        description="Donation amount must be greater than zero."
    )

    message: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    anonymous: bool = False


class DonationResponse(BaseModel):

    id: int
    user_id: int
    gumba_id: int
    amount: float
    message: Optional[str]
    anonymous: bool
    status: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class DonationStatusUpdate(BaseModel):
    status: str = Field(
        description="Donation status: APPROVED or REJECTED"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value = value.upper()

        if value not in ["APPROVED", "REJECTED"]:
            raise ValueError(
                "Status must be APPROVED or REJECTED."
            )

        return value