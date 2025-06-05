from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "customer"  # default role

class UserInDB(UserCreate):
    id: Optional[str] = Field(alias="_id")
