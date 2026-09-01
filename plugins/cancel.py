# plugins/cancel.py

import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from plugins.downloader import cancel_download


logger = logging.getLogger(__name__)


# ============================================================
# /cancel
# ============================================================

@Client.on_message(
    filters.command("cancel")
)
async def cancel_command(
    client: Client,
    message: Message
):

    user = message.from_user

    if not user:
        return

    user_id = user.id

    # --------------------------------------------------------
    # Try to cancel active download
    # --------------------------------------------------------

    cancelled = await cancel_download(
        user_id
    )

    if cancelled:

        await message.reply_text(
            "**ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ.**\n\n"
            "ᴛʜᴇ ᴛᴇᴍᴘᴏʀᴀʀʏ ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴄʟᴇᴀɴᴇᴅ ᴜᴘ."
        )

    else:

        await message.reply_text(
            "**ɴᴏ ᴀᴄᴛɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅ ғᴏᴜɴᴅ.**"
        )
