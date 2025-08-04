from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Exercise(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    sets: int
    reps: int
    weight: float
    restTime: int  # seconds
    completed: bool = False
    completedSets: int = 0
    image: Optional[str] = None

class Workout(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    name: str
    date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"  # pending, active, completed
    progress: float = 0.0  # 0-100
    exercises: List[Exercise] = []
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class WorkoutCreate(BaseModel):
    name: str
    exercises: List[Exercise]

class WorkoutResponse(BaseModel):
    id: str
    name: str
    date: datetime
    status: str
    progress: float
    exercises: List[Exercise]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class CompleteSetRequest(BaseModel):
    setNumber: int
    weight: float
    reps: int

class CompleteSetResponse(BaseModel):
    success: bool
    exercise: dict