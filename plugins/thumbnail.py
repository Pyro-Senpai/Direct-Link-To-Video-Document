import os
import logging
import subprocess

from pyrogram import Client, filters
from pyrogram.types import Message

from config import DOWNLOAD_DIR

logger = logging.getLogger(__name__)


def user_thumbnail_path(user_id):
    return os.path.join(
        DOWNLOAD_DIR,
        f"user_thumb_{user_id}.jpg"
    )


async def save_user_thumbnail(client, message, user_id):
    if not message.reply_to_message:
        return None

    replied = message.reply_to_message

    if not replied.photo:
        return None

    path = user_thumbnail_path(user_id)

    try:
        downloaded = await client.download_media(
            replied,
            file_name=path
        )

        if not downloaded:
            return None

        return path

    except Exception:
        logger.exception("Failed to save user thumbnail")
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
        logger.exception("Failed to delete user thumbnail")
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
            logger.warning(
                "5 second thumbnail failed. Trying random frame."
            )

            command = [
                "ffmpeg",
                "-y",
                "-i",
                filepath,
                "-vf",
                "thumbnail",
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
            logger.error(
                "Automatic thumbnail creation failed: %s",
                result.stderr.decode(errors="ignore")[-1000:]
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
    filters.command("setthumb") & filters.private
)
async def set_thumbnail_command(
    client: Client,
    message: Message
):
    user_id = message.from_user.id

    if not message.reply_to_message:
        await message.reply_text(
            "❌ **Reply to a photo and use `/setthumb`.**"
        )
        return

    if not message.reply_to_message.photo:
        await message.reply_text(
            "❌ **Please reply to a photo.**"
        )
        return

    path = await save_user_thumbnail(
        client,
        message,
        user_id
    )

    if not path:
        await message.reply_text(
            "❌ **Failed to save thumbnail.**"
        )
        return

    await message.reply_text(
        "✅ **Thumbnail set successfully!**\n\n"
        "This thumbnail will be used for your videos."
    )


@Client.on_message(
    filters.command("viewthumb") & filters.private
)
async def view_thumbnail_command(
    client: Client,
    message: Message
):
    user_id = message.from_user.id

    path = get_user_thumbnail(user_id)

    if not path:
        await message.reply_text(
            "ℹ️ **No custom thumbnail is set.**\n\n"
            "Use `/setthumb` by replying to a photo."
        )
        return

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
    filters.command("delthumb") & filters.private
)
async def delete_thumbnail_command(
    client: Client,
    message: Message
):
    user_id = message.from_user.id

    deleted = delete_user_thumbnail(user_id)

    if not deleted:
        await message.reply_text(
            "ℹ️ **You don't have a custom thumbnail.**"
        )
        return

    await message.reply_text(
        "🗑️ **Custom thumbnail deleted.**\n\n"
        "Your videos will now use automatic thumbnails."
    )
