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

@Client.on_message(filters.photo & ~filters.edited)
async def save_photo_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    
    # Download the photo to a local path
    thumb_path = await client.download_media(
        message.photo.file_id,
        file_name=f"thumb_{user_id}.jpg"
    )
    
    if thumb_path and os.path.exists(thumb_path):
        with open(thumb_path, "rb") as f:
            binary_data = f.read()
            
        # Save to database
        await save_thumbnail(user_id, binary_data)
        
        await message.reply_text("✅ **Custom thumbnail saved successfully!**")
        
        # Clean up local file if needed, or keep path depending on database implementation
        try:
            os.remove(thumb_path)
        except Exception:
            pass
    else:
        await message.reply_text("❌ **Failed to save thumbnail. Please try again.**")

@Client.on_message(filters.command("delthumb"))
async def delete_thumb_command(client: Client, message: Message):
    user_id = message.from_user.id
    await delete_thumbnail(user_id)
    await message.reply_text("🗑️ **Custom thumbnail deleted successfully!**")
