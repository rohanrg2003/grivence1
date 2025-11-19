from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr]

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr]
    class Config:
        orm_mode = True

class GrievanceCreate(BaseModel):
    title: str
    description: str

class GrievanceOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    category: Optional[str]
    status: str
    attachment_path: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True
