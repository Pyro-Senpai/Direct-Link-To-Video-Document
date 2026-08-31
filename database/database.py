# database/database.py

import logging
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URI, DATABASE_NAME


logger = logging.getLogger(__name__)


# ============================================================
# MongoDB Connection
# ============================================================

mongo_client = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = mongo_client[DATABASE_NAME]

users_collection = db["users"]
downloads_collection = db["downloads"]


# ============================================================
# Initialize Database
# ============================================================

async def init_db():
    """Connect to MongoDB and create indexes."""

    try:
        await mongo_client.admin.command("ping")

        logger.info("MongoDB connected successfully.")

        # Unique user ID
        await users_collection.create_index(
            "user_id",
            unique=True
        )

        # Download history indexes
        await downloads_collection.create_index(
            "user_id"
        )

        await downloads_collection.create_index(
            "created_at"
        )

        logger.info("MongoDB indexes initialized.")

    except Exception as e:
        logger.error(
            "MongoDB connection failed: %s",
            e
        )
        raise


# ============================================================
# User Functions
# ============================================================

async def add_user(
    user_id: int,
    username: str = None,
    first_name: str = None
):
    """Add a new user or update an existing user."""

    now = datetime.now(timezone.utc)

    await users_collection.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "updated_at": now
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": now,
                "total_downloads": 0
            }
        },
        upsert=True
    )


async def get_user(user_id: int):
    """Get user information."""

    return await users_collection.find_one(
        {"user_id": user_id}
    )


async def user_exists(user_id: int) -> bool:
    """Check if a user exists."""

    user = await users_collection.find_one(
        {"user_id": user_id},
        {"_id": 1}
    )

    return user is not None


async def increment_downloads(user_id: int):
    """Increase user's download count."""

    await users_collection.update_one(
        {"user_id": user_id},
        {
            "$inc": {
                "total_downloads": 1
            }
        }
    )


# ============================================================
# Download History
# ============================================================

async def save_download(
    user_id: int,
    url: str,
    filename: str,
    file_type: str,
    file_size: int = 0
):
    """Save download information."""

    download = {
        "user_id": user_id,
        "url": url,
        "filename": filename,
        "file_type": file_type,
        "file_size": file_size,
        "created_at": datetime.now(timezone.utc)
    }

    result = await downloads_collection.insert_one(
        download
    )

    await increment_downloads(user_id)

    return result.inserted_id


async def get_download_history(
    user_id: int,
    limit: int = 10
):
    """Get user's latest downloads."""

    cursor = (
        downloads_collection
        .find({"user_id": user_id})
        .sort("created_at", -1)
        .limit(limit)
    )

    return await cursor.to_list(
        length=limit
    )


# ============================================================
# Statistics
# ============================================================

async def get_user_count() -> int:
    """Get total number of users."""

    return await users_collection.count_documents({})


async def get_download_count() -> int:
    """Get total number of downloads."""

    return await downloads_collection.count_documents({})


# ============================================================
# Close MongoDB
# ============================================================

async def close_db():
    """Close MongoDB connection."""

    mongo_client.close()

    logger.info(
        "MongoDB connection closed."
    )
