from pydantic import BaseModel, EmailStr, Field
from typing import Optional


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