from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import BaseModelMixin


class AgentApplication(Base, BaseModelMixin):
    __tablename__ = "agent_applications"

    # User who is applying to become an agent
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True
    )

    gumba_id = Column(
        Integer,
        ForeignKey("gumbas.id"),
        nullable=True,
        index=True
    )
    gumba_application_type = Column(
        String(20),
        nullable=False
    )

    # Profile information
    profile_photo = Column(String(500), nullable=True)

    gender = Column(String(20), nullable=True)

    address = Column(
        String(255),
        nullable=False
    )

    district = Column(
        String(100),
        nullable=False
    )

    municipality = Column(
        String(100),
        nullable=False
    )

    ward_no = Column(
        String(20),
        nullable=False
    )

    designation = Column(
        String(100),
        nullable=False
    )

    short_bio = Column(
        Text,
        nullable=True
    )

    # Verification information
    id_type = Column(
        String(50),
        nullable=False
    )

    id_number = Column(
        String(100),
        nullable=False
    )

    id_document = Column(
        String(500),
        nullable=False
    )

    gumba_association_letter = Column(
        String(500),
        nullable=False
    )

    # PENDING / APPROVED / REJECTED
    verification_status = Column(
        String(20),
        nullable=False,
        default="PENDING",
        index=True
    )

    # Relationship with applicant
    user = relationship(
        "User",
        back_populates="agent_application"
    )

    gumba = relationship(
        "Gumba",
        back_populates="agent_applications"
    )
    new_gumba_name = Column(String(100), nullable=True)

    new_gumba_description = Column(Text, nullable=True)

    new_gumba_address = Column(String(255), nullable=True)

    new_gumba_district = Column(String(100), nullable=True)

    new_gumba_municipality = Column(String(100), nullable=True)

    new_gumba_ward_no = Column(String(20), nullable=True)

    new_gumba_contact_phone = Column(String(20), nullable=True)

    new_gumba_contact_email = Column(String(255), nullable=True)

    new_gumba_website = Column(String(255), nullable=True)

    new_gumba_latitude = Column(Float, nullable=True)

    new_gumba_longitude = Column(Float, nullable=True)