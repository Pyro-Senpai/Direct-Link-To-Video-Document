import logging
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_URI, DATABASE_NAME


logger = logging.getLogger(__name__)


mongo_client = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = mongo_client[DATABASE_NAME]

users_collection = db["users"]
downloads_collection = db["downloads"]


async def init_db():
    try:
        await mongo_client.admin.command("ping")

        logger.info(
            "MongoDB connected successfully."
        )

        await users_collection.create_index(
            "user_id",
            unique=True
        )

        await downloads_collection.create_index(
            "user_id"
        )

        await downloads_collection.create_index(
            "created_at"
        )

        logger.info(
            "MongoDB indexes initialized."
        )

    except Exception as e:
        logger.error(
            "MongoDB connection failed: %s",
            e
        )
        raise


async def add_user(
    user_id: int,
    username: str = None,
    first_name: str = None
):
    now = datetime.now(timezone.utc)

    await users_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "updated_at": now
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": now,
                "total_downloads": 0,
                "thumbnail": None,
                "caption": None
            }
        },
        upsert=True
    )


async def get_user(user_id: int):
    return await users_collection.find_one(
        {
            "user_id": user_id
        }
    )


async def user_exists(user_id: int) -> bool:
    user = await users_collection.find_one(
        {
            "user_id": user_id
        },
        {
            "_id": 1
        }
    )

    return user is not None


async def increment_downloads(
    user_id: int
):
    await users_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$inc": {
                "total_downloads": 1
            }
        },
        upsert=True
    )


async def set_thumbnail(
    user_id: int,
    file_id = None
):
    await users_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "thumbnail": file_id,
                "updated_at": datetime.now(timezone.utc)
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc),
                "total_downloads": 0
            }
        },
        upsert=True
    )


async def save_thumbnail(
    user_id: int,
    file_id = None
):
    await set_thumbnail(user_id, file_id)


async def get_thumbnail(
    user_id: int
):
    user = await users_collection.find_one(
        {
            "user_id": user_id
        },
        {
            "thumbnail": 1
        }
    )

    if not user:
        return None

    return user.get("thumbnail")


async def delete_thumbnail(
    user_id: int
):
    await users_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "thumbnail": None,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )


async def set_caption(
    user_id: int,
    caption: str = None
):
    await users_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "caption": caption,
                "updated_at": datetime.now(timezone.utc)
            },
            "$setOnInsert": {
                "user_id": user_id,
                "created_at": datetime.now(timezone.utc),
                "total_downloads": 0
            }
        },
        upsert=True
    )


async def get_caption(
    user_id: int
):
    user = await users_collection.find_one(
        {
            "user_id": user_id
        },
        {
            "caption": 1
        }
    )

    if not user:
        return None

    return user.get("caption")


async def save_download(
    user_id: int,
    url: str,
    filename: str,
    file_type: str,
    file_size: int = 0
):
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

    await increment_downloads(
        user_id
    )

    return result.inserted_id


async def get_download_history(
    user_id: int,
    limit: int = 10
):
    cursor = (
        downloads_collection
        .find(
            {
                "user_id": user_id
            }
        )
        .sort(
            "created_at",
            -1
        )
        .limit(limit)
    )

    return await cursor.to_list(
        length=limit
    )


async def get_user_count() -> int:
    return await users_collection.count_documents({})


async def get_download_count() -> int:
    return await downloads_collection.count_documents({})


async def close_db():
    mongo_client.close()

    logger.info(
        "MongoDB connection closed."
    )
