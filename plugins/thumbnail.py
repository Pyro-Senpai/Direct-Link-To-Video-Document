import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import save_thumbnail, get_thumbnail, delete_thumbnail

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("setthumb"))
async def set_thumb_command(client: Client, message: Message):
    await message.reply_text(
        "🖼️ **Please send your thumbnail photo now.**\n\n"
        "It will be saved automatically as your custom thumbnail."
    )

@Client.on_message(filters.photo & filters.incoming)
async def save_photo_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    
    thumb_path = await client.download_media(
        message.photo.file_id,
        file_name=f"thumb_{user_id}.jpg"
    )
    
    if thumb_path and os.path.exists(thumb_path):
        with open(thumb_path, "rb") as f:
            binary_data = f.read()
            
        await save_thumbnail(user_id, binary_data)
        
        await message.reply_text("✅ **Custom thumbnail saved successfully!**")
        
        try:
            os.remove(thumb_path)
        except Exception:
            pass
    else:
        await message.reply_text("❌ **Failed to save thumbnail. Please try again.**")

@Client.on_message(filters.command("viewthumb"))
async def view_thumb_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    try:
        thumbnail = await get_thumbnail(user_id)
        
        if not thumbnail:
            await message.reply_text("❌ **You don't have a custom thumbnail saved.**")
            return

        thumb_path = f"view_thumb_{user_id}.jpg"
        
        if isinstance(thumbnail, bytes):
            with open(thumb_path, "wb") as f:
                f.write(thumbnail)
        elif isinstance(thumbnail, str) and os.path.exists(thumbnail):
            thumb_path = thumbnail
        else:
            await message.reply_text("❌ **Could not retrieve your custom thumbnail.**")
            return

        await client.send_photo(
            chat_id=message.chat.id,
            photo=thumb_path,
            caption="🖼️ **Your Current Custom Thumbnail**"
        )

        if thumb_path.startswith("view_thumb_") and os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception:
        logger.exception("Failed to view thumbnail.")
        await message.reply_text("❌ **An error occurred while fetching your thumbnail.**")

@Client.on_message(filters.command("delthumb"))
async def delete_thumb_command(client: Client, message: Message):
    user_id = message.from_user.id
    await delete_thumbnail(user_id)
    await message.reply_text("🗑️ **Custom thumbnail deleted successfully!**")
