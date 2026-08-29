from sqlalchemy import Column, String, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship

from app.models.base import BaseModelMixin
from app.core.database import Base

class Gumba(Base, BaseModelMixin):
    __tablename__ = "gumbas"

    name = Column(String(100), nullable=False, index=True)

    description = Column(Text, nullable=True)

    address = Column(String(255), nullable=False)

    district = Column(String(100), nullable=False)

    municipality = Column(String(100), nullable=True)

    ward_no = Column(String(20), nullable=True)

    contact_phone = Column(String(15), nullable=True)

    contact_email = Column(String(255), nullable=True)

    website = Column(String(255), nullable=True)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    # Multiple photos/videos can be stored as URLs
    photos = Column(JSON, nullable=True)

    videos = Column(JSON, nullable=True)

    # One Gumba -> One Agent
    agent_id = Column(
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    agent = relationship(
        "User",
        back_populates="gumbas"
    )
    
    donations = relationship(
        "Donation",
        back_populates="gumba"
    )