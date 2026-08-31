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
            "❌ **Download cancelled.**\n\n"
            "The temporary file will be cleaned up."
        )

    else:

        await message.reply_text(
            "ℹ️ **No active download found.**"
        )
