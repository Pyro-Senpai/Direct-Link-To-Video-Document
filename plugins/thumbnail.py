import os
import logging
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)

def user_thumbnail_path(user_id):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    return os.path.join(
        DOWNLOAD_DIR,
        f"user_thumb_{user_id}.jpg"
    )

async def save_user_thumbnail_direct(client, message, user_id):
    if not message.photo:
        return None

    path = user_thumbnail_path(user_id)

    try:
        downloaded = await client.download_media(
            message,
            file_name=path
        )

        if not downloaded:
            return None

        return path

    except Exception:
        logger.exception(
            "Failed to save user thumbnail"
        )
        return None

def get_user_thumbnail(user_id):
    path = user_thumbnail_path(user_id)

    if os.path.exists(path):
        return path

    return None

def delete_user_thumbnail(user_id):
    path = user_thumbnail_path(user_id)

    if not os.path.exists(path):
        return False

    try:
        os.remove(path)
        return True

    except Exception:
        logger.exception(
            "Failed to delete user thumbnail"
        )
        return False

def create_video_thumbnail(filepath, output_path=None):
    if not filepath:
        return None

    if not os.path.exists(filepath):
        return None

    if output_path is None:
        output_path = os.path.join(
            DOWNLOAD_DIR,
            f"auto_thumb_{os.path.basename(filepath)}.jpg"
        )

    try:
        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        command = [
            "ffmpeg",
            "-y",
            "-ss",
            "00:05",
            "-i",
            filepath,
            "-frames:v",
            "1",
            "-vf",
            "scale=320:320:force_original_aspect_ratio=decrease",
            "-q:v",
            "3",
            output_path
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        if result.returncode != 0:
            command = [
                "ffmpeg",
                "-y",
                "-i",
                filepath,
                "-vf",
                "thumbnail,scale=320:320:force_original_aspect_ratio=decrease",
                "-frames:v",
                "1",
                "-q:v",
                "3",
                output_path
            ]

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=60
            )

        if result.returncode != 0:
            logger.error(
                "Automatic thumbnail creation failed: %s",
                result.stderr.decode(
                    errors="ignore"
                )[-1000:]
            )
            return None

        if not os.path.exists(output_path):
            return None

        if os.path.getsize(output_path) <= 0:
            return None

        return output_path

    except Exception:
        logger.exception(
            "Automatic thumbnail creation failed"
        )
        return None

@Client.on_message(
    filters.private &
    filters.command(["setthumb", "set_thumb"])
)
async def set_thumbnail_command(
    client: Client,
    message: Message
):
    await message.reply_text(
        "🖼️ **Please send your thumbnail photo now.**\n\n"
        "It will be saved automatically as your custom thumbnail."
    )

@Client.on_message(
    filters.private &
    filters.photo &
    ~filters.command(["setthumb", "set_thumb", "viewthumb", "view_thumb", "delthumb", "del_thumb"])
)
async def auto_save_thumbnail_handler(
    client: Client,
    message: Message
):
    user_id = message.from_user.id
    
    status = await message.reply_text(
        "⏳ **Saving thumbnail...**"
    )

    path = await save_user_thumbnail_direct(
        client,
        message,
        user_id
    )

    if not path:
        return await status.edit_text(
            "❌ **Failed to save thumbnail.**"
        )

    await status.edit_text(
        "✅ **Thumbnail set successfully!**\n\n"
        "Your custom thumbnail will be used for your videos."
    )

@Client.on_message(
    filters.private &
    filters.command(["viewthumb", "view_thumb"])
)
async def view_thumbnail_command(
    client: Client,
    message: Message
):
    user_id = message.from_user.id

    path = get_user_thumbnail(user_id)

    if not path:
        return await message.reply_text(
            "😔 **You don't have any thumbnail.**\n\n"
            "Just send a photo to set a new thumbnail."
        )

    try:
        await message.reply_photo(
            photo=path,
            caption="🖼️ **Your current thumbnail**"
        )

    except Exception:
        logger.exception(
            "Failed to show thumbnail"
        )

        await message.reply_text(
            "❌ **Failed to show thumbnail.**"
        )

@Client.on_message(
    filters.private &
    filters.command(["delthumb", "del_thumb"])
)
async def delete_thumbnail_command(
    client: Client,
    message: Message
):
    user_id = message.from_user.id

    deleted = delete_user_thumbnail(user_id)

    if not deleted:
        return await message.reply_text(
            "😔 **You don't have any thumbnail.**"
        )

    await message.reply_text(
        "❌ **Thumbnail deleted successfully.**\n\n"
        "Your videos will now use automatic thumbnails."
    )
