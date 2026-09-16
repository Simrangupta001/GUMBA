from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin


class User(Base, BaseModelMixin):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    profile_photo = Column(String(500), nullable=True)
    address = Column(String(255), nullable=True)
    district = Column(String(100), nullable=True)
    municipality = Column(String(100), nullable=True)
    ward_no = Column(String(20), nullable=True)
    role = relationship("Role")
    gumbas = relationship("Gumba", back_populates="agent")
    donations = relationship("Donation", back_populates="user")
  
    agent_application = relationship(
        "AgentApplication",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


