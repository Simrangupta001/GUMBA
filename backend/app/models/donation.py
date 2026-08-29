from sqlalchemy import Column, Integer, Float, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModelMixin
from app.core.database import Base


class Donation(Base, BaseModelMixin):
    __tablename__ = "donations"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    gumba_id = Column(
        Integer,
        ForeignKey("gumbas.id"),
        nullable=False,
        index=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    message = Column(
        Text,
        nullable=True
    )

    anonymous = Column(
        Boolean,
        default=False,
        nullable=False
    )

    status = Column(
        String(20),
        default="PENDING",
        nullable=False,
        index=True
    )

    user = relationship(
        "User",
        back_populates="donations"
    )

    gumba = relationship(
        "Gumba",
        back_populates="donations"
    )