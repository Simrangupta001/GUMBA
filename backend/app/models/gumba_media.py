from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class GumbaMedia(Base):
    __tablename__ = "gumba_media"

    id = Column(Integer, primary_key=True, index=True)

    gumba_id = Column(
        Integer,
        ForeignKey("gumbas.id", ondelete="CASCADE"),
        nullable=False
    )

    media_type = Column(
        String(20),
        nullable=False
    )

    media_url = Column(
        String(500),
        nullable=False
    )

    gumba = relationship(
        "Gumba",
        back_populates="media"
    )