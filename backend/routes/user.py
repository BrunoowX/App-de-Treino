from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserResponse
from auth.dependencies import get_current_user
from database import get_database
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/profile", response_model=UserResponse)
async def get_profile(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get user profile"""
    try:
        user_doc = await db.users.find_one({"id": current_user["user_id"]})
        if not user_doc:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return UserResponse(
            id=user_doc["id"],
            name=user_doc["name"],
            email=user_doc["email"],
            avatar=user_doc.get("avatar"),
            totalWorkouts=user_doc.get("totalWorkouts", 0),
            streak=user_doc.get("streak", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")