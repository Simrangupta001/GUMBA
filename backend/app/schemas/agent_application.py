from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from app.enums.agent_application import GumbaApplicationType


class AgentApplicationCreate(BaseModel):

    # ---------------------------------------------------------
    # GUMBA APPLICATION
    # ---------------------------------------------------------

    gumba_application_type: GumbaApplicationType

    # Required when selecting an existing Gumba.
    # Must be NULL when registering a new Gumba.
    gumba_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    # ---------------------------------------------------------
    # NEW GUMBA INFORMATION
    # Used only when gumba_application_type = NEW
    # ---------------------------------------------------------

    new_gumba_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    new_gumba_description: Optional[str] = Field(
        default=None,
        max_length=2000
    )

    new_gumba_address: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    new_gumba_district: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    new_gumba_municipality: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    new_gumba_ward_no: Optional[int] = Field(
        default=None,
        ge=1
    )

    new_gumba_contact_phone: Optional[str] = None

    new_gumba_contact_email: Optional[str] = None

    new_gumba_website: Optional[str] = None

    new_gumba_latitude: Optional[float] = None

    new_gumba_longitude: Optional[float] = None

    # ---------------------------------------------------------
    # APPLICANT PROFILE
    # ---------------------------------------------------------

    gender: Optional[str] = Field(
        default=None,
        max_length=20
    )

    address: str = Field(
        min_length=3,
        max_length=100
    )

    district: str = Field(
        min_length=2,
        max_length=100
    )

    municipality: str = Field(
        min_length=2,
        max_length=100
    )

    ward_no: int = Field(
        ge=1
    )

    designation: str = Field(
        min_length=2,
        max_length=100
    )

    short_bio: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=300
    )

    # ---------------------------------------------------------
    # IDENTITY VERIFICATION
    # ---------------------------------------------------------

    id_type: str = Field(
        min_length=2,
        max_length=50
    )

    id_number: str = Field(
        min_length=2,
        max_length=100
    )

    # ---------------------------------------------------------
    # COMMON TEXT NORMALIZATION
    # ---------------------------------------------------------

    @field_validator(
        "address",
        "district",
        "municipality",
        "designation",
        "id_type",
        "id_number",
        mode="before"
    )
    @classmethod
    def normalize_text(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty.")

        return value

    # ---------------------------------------------------------
    # NEW GUMBA TEXT NORMALIZATION
    # ---------------------------------------------------------

    @field_validator(
        "new_gumba_name",
        "new_gumba_description",
        "new_gumba_address",
        "new_gumba_district",
        "new_gumba_municipality",
        "new_gumba_contact_phone",
        "new_gumba_contact_email",
        "new_gumba_website",
        mode="before"
    )
    @classmethod
    def normalize_new_gumba_fields(cls, value):
        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

        return value

    # ---------------------------------------------------------
    # CONDITIONAL GUMBA VALIDATION
    # ---------------------------------------------------------

    @model_validator(mode="after")
    def validate_gumba_application(self):

        if self.gumba_application_type == GumbaApplicationType.EXISTING:

            if self.gumba_id is None:
                raise ValueError(
                    "gumba_id is required when selecting an existing Gumba."
                )

            new_gumba_fields = {
                "new_gumba_name": self.new_gumba_name,
                "new_gumba_description": self.new_gumba_description,
                "new_gumba_address": self.new_gumba_address,
                "new_gumba_district": self.new_gumba_district,
                "new_gumba_municipality": self.new_gumba_municipality,
                "new_gumba_ward_no": self.new_gumba_ward_no,
                "new_gumba_contact_phone": self.new_gumba_contact_phone,
                "new_gumba_contact_email": self.new_gumba_contact_email,
                "new_gumba_website": self.new_gumba_website,
                "new_gumba_latitude": self.new_gumba_latitude,
                "new_gumba_longitude": self.new_gumba_longitude,
            }

            if any(value is not None for value in new_gumba_fields.values()):
                raise ValueError(
                    "New Gumba information must not be provided when "
                    "selecting an existing Gumba."
                )

        elif self.gumba_application_type == GumbaApplicationType.NEW:

            if self.gumba_id is not None:
                raise ValueError(
                    "gumba_id must not be provided when registering a new Gumba."
                )

            required_fields = {
                "new_gumba_name": self.new_gumba_name,
                "new_gumba_address": self.new_gumba_address,
                "new_gumba_district": self.new_gumba_district,
                "new_gumba_municipality": self.new_gumba_municipality,
                "new_gumba_ward_no": self.new_gumba_ward_no,
            }

            missing_fields = [
                field
                for field, value in required_fields.items()
                if value is None
            ]

            if missing_fields:
                raise ValueError(
                    "The following fields are required for a new Gumba: "
                    + ", ".join(missing_fields)
                )

        return self


class AgentApplicationResponse(BaseModel):

    id: int
    user_id: int

    profile_photo: Optional[str]
    gender: Optional[str]

    address: str
    district: str
    municipality: str
    ward_no: int

    designation: str
    short_bio: Optional[str]

    id_type: str

    verification_status: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )