# plugins/start.py

import re
import logging

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.database import add_user
from plugins.callbacks import create_download_request


logger = logging.getLogger(__name__)


# ============================================================
# URL Pattern
# ============================================================

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE
)


# ============================================================
# /start
# ============================================================

@Client.on_message(
    filters.command("start")
)
async def start_command(
    client: Client,
    message: Message
):

    user = message.from_user

    if not user:
        return

    # --------------------------------------------------------
    # Save user to MongoDB
    # --------------------------------------------------------

    try:

        await add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name
        )

    except Exception as e:

        logger.error(
            "Failed to save user: %s",
            e
        )


    # --------------------------------------------------------
    # Welcome Message
    # --------------------------------------------------------

    text = (
        "👋 **Welcome to Direct Link Downloader!**\n\n"

        "🔗 Send me a direct download link and "
        "I'll download the file for you.\n\n"

        "━━━━━━━━━━━━━━━━━━━━\n\n"

        "🎬 **Video**\n"
        "Send supported video files as Telegram video.\n\n"

        "📁 **Document**\n"
        "Send the file as a Telegram document.\n\n"

        "━━━━━━━━━━━━━━━━━━━━\n\n"

        "📌 **How to use:**\n\n"
        "1️⃣ Send a direct download URL\n"
        "2️⃣ Choose **Video** or **Document**\n"
        "3️⃣ Wait for the download\n"
        "4️⃣ Receive your file\n\n"

        "📦 Maximum download size: **4 GB**\n\n"

        "❌ Use `/cancel` to cancel an active download."
    )

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )


# ============================================================
# URL Handler
# ============================================================

@Client.on_message(
    filters.text
    & ~filters.command(
        ["start", "cancel"]
    )
)
async def url_handler(
    client: Client,
    message: Message
):

    user = message.from_user

    if not user:
        return

    text = message.text or ""

    # --------------------------------------------------------
    # Find URL
    # --------------------------------------------------------

    match = URL_PATTERN.search(text)

    if not match:

        await message.reply_text(
            "❌ **No valid URL found.**\n\n"
            "Please send a direct download link."
        )

        return


    url = match.group(0).rstrip(
        ".,!?)]}>"
    )


    # --------------------------------------------------------
    # Save User
    # --------------------------------------------------------

    try:

        await add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name
        )

    except Exception as e:

        logger.error(
            "Failed to save user: %s",
            e
        )


    # --------------------------------------------------------
    # Create Short Download ID
    # --------------------------------------------------------

    short_id = create_download_request(
        user_id=user.id,
        url=url
    )


    # --------------------------------------------------------
    # Buttons
    # --------------------------------------------------------

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Video",
                    callback_data=f"video:{short_id}"
                ),

                InlineKeyboardButton(
                    "📁 Document",
                    callback_data=f"document:{short_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel_download"
                )
            ]
        ]
    )


    # --------------------------------------------------------
    # Reply
    # --------------------------------------------------------

    await message.reply_text(
        "🔗 **Link detected!**\n\n"
        "Choose how you want me to send the file:",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )
