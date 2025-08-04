from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user import UserCreate, UserLogin, AuthResponse, User, UserResponse
from auth.password import hash_password, verify_password
from auth.jwt_handler import create_access_token
from database import get_database
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=AuthResponse)
async def register(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            avatar=f"https://ui-avatars.com/api/?name={user_data.name.replace(' ', '+')}&background=ef4444&color=fff"
        )
        
        # Save to database
        user_dict = user.dict()
        user_dict["passwordHash"] = hashed_password
        result = await db.users.insert_one(user_dict)
        
        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")
        
        # Create JWT token
        token = create_access_token({"user_id": user.id, "email": user.email})
        
        # Return response
        user_response = UserResponse(**user.dict())
        return AuthResponse(success=True, user=user_response, token=token)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.post("/login", response_model=AuthResponse)
async def login(login_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_database)):
    """Login user"""
    try:
        # Find user by email
        user_doc = await db.users.find_one({"email": login_data.email})
        if not user_doc:
            raise HTTPException(status_code=401, detail="Email ou senha incorretos")
        
        # Verify password
        if not verify_password(login_data.password, user_doc["passwordHash"]):
            raise HTTPException(status_code=401, detail="Email ou senha incorretos")
        
        # Create JWT token
        token = create_access_token({"user_id": user_doc["id"], "email": user_doc["email"]})
        
        # Prepare user response
        user_response = UserResponse(
            id=user_doc["id"],
            name=user_doc["name"],
            email=user_doc["email"],
            avatar=user_doc.get("avatar"),
            totalWorkouts=user_doc.get("totalWorkouts", 0),
            streak=user_doc.get("streak", 0)
        )
        
        return AuthResponse(success=True, user=user_response, token=token)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")