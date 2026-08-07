from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, ConfigDict

class AdminCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    password: str

class AdminResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)