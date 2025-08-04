from pydantic import BaseModel
from typing import List
from datetime import datetime

class WeeklyProgress(BaseModel):
    week: str
    volume: float
    weight: float
    workouts: int

class ProgressStats(BaseModel):
    totalVolume: float
    avgWeight: float
    completedWorkouts: int
    currentStreak: int

class WorkoutSession(BaseModel):
    id: str
    userId: str
    workoutId: str
    exercises: List[dict]
    startedAt: datetime
    completedAt: datetime = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }