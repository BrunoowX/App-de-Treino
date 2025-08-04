from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os
import logging

logger = logging.getLogger(__name__)

# MongoDB connection
client = None
database = None

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    try:
        mongo_url = os.environ.get('MONGO_URL')
        db_name = os.environ.get('DB_NAME', 'fitness_app')
        
        client = AsyncIOMotorClient(mongo_url)
        database = client[db_name]
        
        # Test connection
        await database.command("ping")
        logger.info("Connected to MongoDB successfully")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        logger.info("Disconnected from MongoDB")

def get_database() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return database