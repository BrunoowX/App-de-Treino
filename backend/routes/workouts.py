from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List
from models.workout import Workout, WorkoutResponse, CompleteSetRequest, CompleteSetResponse
from auth.dependencies import get_current_user
from database import get_database
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/workouts", tags=["workouts"])

# Sample workout templates
SAMPLE_WORKOUTS = [
    {
        "name": "Peito e Tríceps",
        "exercises": [
            {
                "name": "Supino Reto",
                "sets": 4,
                "reps": 10,
                "weight": 80,
                "restTime": 90,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            },
            {
                "name": "Supino Inclinado",
                "sets": 4,
                "reps": 8,
                "weight": 70,
                "restTime": 90,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            },
            {
                "name": "Crucifixo",
                "sets": 3,
                "reps": 12,
                "weight": 25,
                "restTime": 60,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            },
            {
                "name": "Tríceps Testa",
                "sets": 4,
                "reps": 12,
                "weight": 30,
                "restTime": 60,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            }
        ]
    },
    {
        "name": "Costas e Bíceps",
        "exercises": [
            {
                "name": "Puxada Frontal",
                "sets": 4,
                "reps": 10,
                "weight": 65,
                "restTime": 90,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            },
            {
                "name": "Remada Baixa",
                "sets": 4,
                "reps": 10,
                "weight": 60,
                "restTime": 90,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            },
            {
                "name": "Rosca Direta",
                "sets": 3,
                "reps": 12,
                "weight": 20,
                "restTime": 60,
                "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=80&h=80&fit=crop"
            }
        ]
    }
]

async def initialize_user_workouts(db: AsyncIOMotorDatabase, user_id: str):
    """Initialize sample workouts for new user"""
    try:
        # Check if user already has workouts
        existing_workouts = await db.workouts.count_documents({"userId": user_id})
        if existing_workouts > 0:
            return
        
        # Create sample workouts
        for i, template in enumerate(SAMPLE_WORKOUTS):
            workout = Workout(
                userId=user_id,
                name=template["name"],
                date=datetime.utcnow() + timedelta(days=i),
                status="active" if i == 0 else "pending",
                exercises=[
                    {
                        "id": f"ex_{j}",
                        "name": ex["name"],
                        "sets": ex["sets"],
                        "reps": ex["reps"],
                        "weight": ex["weight"],
                        "restTime": ex["restTime"],
                        "completed": False,
                        "completedSets": 0,
                        "image": ex["image"]
                    }
                    for j, ex in enumerate(template["exercises"])
                ]
            )
            await db.workouts.insert_one(workout.dict())
            
    except Exception as e:
        logger.error(f"Error initializing workouts: {str(e)}")

@router.get("/", response_model=List[WorkoutResponse])
async def get_workouts(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all workouts for current user"""
    try:
        user_id = current_user["user_id"]
        
        # Initialize workouts if user has none
        await initialize_user_workouts(db, user_id)
        
        # Get workouts
        workouts = await db.workouts.find({"userId": user_id}).sort("date", 1).to_list(100)
        
        return [
            WorkoutResponse(
                id=workout["id"],
                name=workout["name"],
                date=workout["date"],
                status=workout["status"],
                progress=workout["progress"],
                exercises=workout["exercises"]
            )
            for workout in workouts
        ]
        
    except Exception as e:
        logger.error(f"Get workouts error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/today", response_model=WorkoutResponse)
async def get_today_workout(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get today's workout"""
    try:
        user_id = current_user["user_id"]
        
        # Initialize workouts if user has none
        await initialize_user_workouts(db, user_id)
        
        # Find active workout
        workout = await db.workouts.find_one({
            "userId": user_id,
            "status": "active"
        })
        
        if not workout:
            # If no active workout, make the first pending workout active
            workout = await db.workouts.find_one({
                "userId": user_id,
                "status": "pending"
            })
            if workout:
                await db.workouts.update_one(
                    {"id": workout["id"]},
                    {"$set": {"status": "active"}}
                )
                workout["status"] = "active"
        
        if not workout:
            raise HTTPException(status_code=404, detail="Nenhum treino encontrado para hoje")
        
        return WorkoutResponse(
            id=workout["id"],
            name=workout["name"],
            date=workout["date"],
            status=workout["status"],
            progress=workout["progress"],
            exercises=workout["exercises"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get today workout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/{workout_id}/exercises/{exercise_id}/complete-set", response_model=CompleteSetResponse)
async def complete_set(
    workout_id: str,
    exercise_id: str,
    set_data: CompleteSetRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Complete a set for an exercise"""
    try:
        user_id = current_user["user_id"]
        
        # Find workout
        workout = await db.workouts.find_one({"id": workout_id, "userId": user_id})
        if not workout:
            raise HTTPException(status_code=404, detail="Treino não encontrado")
        
        # Find exercise
        exercise_index = None
        for i, ex in enumerate(workout["exercises"]):
            if ex["id"] == exercise_id:
                exercise_index = i
                break
        
        if exercise_index is None:
            raise HTTPException(status_code=404, detail="Exercício não encontrado")
        
        # Update exercise
        exercise = workout["exercises"][exercise_index]
        exercise["completedSets"] = min(exercise["completedSets"] + 1, exercise["sets"])
        
        if exercise["completedSets"] >= exercise["sets"]:
            exercise["completed"] = True
        
        # Calculate workout progress
        completed_exercises = sum(1 for ex in workout["exercises"] if ex["completed"])
        progress = (completed_exercises / len(workout["exercises"])) * 100
        
        # Update workout status
        status = workout["status"]
        if progress >= 100:
            status = "completed"
            # Update user stats
            await db.users.update_one(
                {"id": user_id},
                {"$inc": {"totalWorkouts": 1, "streak": 1}}
            )
        
        # Save changes
        await db.workouts.update_one(
            {"id": workout_id},
            {
                "$set": {
                    "exercises": workout["exercises"],
                    "progress": progress,
                    "status": status
                }
            }
        )
        
        return CompleteSetResponse(
            success=True,
            exercise={
                "id": exercise_id,
                "completedSets": exercise["completedSets"],
                "totalSets": exercise["sets"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Complete set error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")