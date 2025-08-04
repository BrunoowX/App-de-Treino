from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# Import routes
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.workouts import router as workouts_router
from routes.progress import router as progress_router

# Import database
from database import connect_to_mongo, close_mongo_connection

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Fitness App API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "Fitness App API is running", "status": "healthy"}

# Include route routers
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(workouts_router)
api_router.include_router(progress_router)

# Include the main router in the app
app.include_router(api_router)

@app.on_event("startup")
async def startup_db_client():
    """Connect to database on startup"""
    await connect_to_mongo()
    logger.info("Fitness App API started successfully")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    await close_mongo_connection()
    logger.info("Fitness App API shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)