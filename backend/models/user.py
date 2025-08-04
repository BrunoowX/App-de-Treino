from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    avatar: Optional[str] = None
    totalWorkouts: int = 0
    streak: int = 0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    avatar: Optional[str] = None
    totalWorkouts: int
    streak: int

class AuthResponse(BaseModel):
    success: bool
    user: UserResponse
    token: str