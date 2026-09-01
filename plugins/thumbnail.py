import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import save_thumbnail, get_thumbnail, delete_thumbnail

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("setthumb"))
async def set_thumb_command(client: Client, message: Message):
    await message.reply_text(
        "**ᴘʟᴇᴀsᴇ sᴇɴsᴇɴʏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ ᴘʜᴏᴛᴏ nᴏᴡ.**\n\n"
        "ɪᴛ wɪʟʟ ʙᴇ sᴀᴠᴇᴅ aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ as ʏᴏᴜʀ cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ."
    )

@Client.on_message(filters.photo & filters.incoming)
async def save_photo_thumbnail(client: Client, message: Message):
    user_id = message.from_user.id
    
    thumb_path = await client.download_media(
        message,
        file_name=f"thumb_{user_id}.jpg"
    )
    
    if thumb_path and os.path.exists(thumb_path):
        with open(thumb_path, "rb") as f:
            binary_data = f.read()
            
        await save_thumbnail(user_id, binary_data)
        
        await message.reply_text("**ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")
        
        try:
            os.remove(thumb_path)
        except Exception:
            pass
    else:
        await message.reply_text("**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴀᴠᴇ ᴛʜᴜᴍʙɴᴀɪʟ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ.**")

@Client.on_message(filters.command("viewthumb"))
async def view_thumb_command(client: Client, message: Message):
    user_id = message.from_user.id
    
    try:
        thumbnail = await get_thumbnail(user_id)
        
        if not thumbnail:
            await message.reply_text("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ a ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ sᴀᴠᴇᴅ.**")
            return

        thumb_path = f"view_thumb_{user_id}.jpg"
        
        if isinstance(thumbnail, bytes):
            with open(thumb_path, "wb") as f:
                f.write(thumbnail)
        elif isinstance(thumbnail, str) and os.path.exists(thumbnail):
            thumb_path = thumbnail
        else:
            await message.reply_text("**ᴄᴏᴜʟᴅ nᴏᴛ rᴇᴛʀɪᴇᴠᴇ ʏᴏᴜʀ cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ.**")
            return

        await client.send_photo(
            chat_id=message.chat.id,
            photo=thumb_path,
            caption="**ʏᴏᴜʀ cᴜʀʀᴇɴᴛ cᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ**"
        )

        if thumb_path.startswith("view_thumb_") and os.path.exists(thumb_path):
            os.remove(thumb_path)

    except Exception:
        logger.exception("Failed to view thumbnail.")
        await message.reply_text("**ᴀɴ eʀʀᴏʀ oᴄᴄᴜʀʀᴇᴅ wʜɪʟᴇ ғᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ᴛʜᴜᴍʙɴᴀɪʟ.**")

@Client.on_message(filters.command("delthumb"))
async def delete_thumb_command(client: Client, message: Message):
    user_id = message.from_user.id
    await delete_thumbnail(user_id)
    await message.reply_text("**ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ dᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ!**")
