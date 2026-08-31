import re

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import START_IMAGE


# ============================================================
# START KEYBOARD
# ============================================================

def start_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❓ Help",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "ℹ️ About",
                    callback_data="about"
                )
            ]
        ]
    )


# ============================================================
# START MESSAGE
# ============================================================

START_TEXT = (
    "👋 **Hello!**\n\n"
    "🔗 Send me a direct download link "
    "and I'll download the file for you.\n\n"
    "📥 Supports **Video** and **Document**."
)


# ============================================================
# /START
# ============================================================

@Client.on_message(
    filters.command("start")
    & filters.private
)
async def start_command(
    client: Client,
    message: Message
):

    keyboard = start_keyboard()

    # --------------------------------------------------------
    # SEND START IMAGE
    # --------------------------------------------------------

    if START_IMAGE:

        try:

            await message.reply_photo(
                photo=START_IMAGE,
                caption=START_TEXT,
                reply_markup=keyboard
            )

            return

        except Exception:

            # If image URL is invalid, fall back
            # to normal text message.
            pass

    # --------------------------------------------------------
    # TEXT FALLBACK
    # --------------------------------------------------------

    await message.reply_text(
        START_TEXT,
        reply_markup=keyboard
    )


# ============================================================
# URL HANDLER
# ============================================================

@Client.on_message(
    filters.private
    & filters.text
    & ~filters.command(
        [
            "start",
            "cancel"
        ]
    )
)
async def url_handler(
    client: Client,
    message: Message
):

    url = message.text.strip()

    # --------------------------------------------------------
    # VALIDATE URL
    # --------------------------------------------------------

    if not re.match(
        r"^https?://",
        url,
        re.IGNORECASE
    ):

        await message.reply_text(
            "❌ **Please send a valid HTTP/HTTPS URL.**"
        )

        return

    # --------------------------------------------------------
    # VERY LONG URL CHECK
    # --------------------------------------------------------
    #
    # The URL is temporarily placed in callback_data.
    # Telegram has a callback_data size limit.
    #
    # --------------------------------------------------------

    if len(
        url.encode("utf-8")
    ) > 150:

        await message.reply_text(
            "❌ **This URL is too long.**\n\n"
            "Please send a shorter direct download URL."
        )

        return

    # --------------------------------------------------------
    # SHOW VIDEO / DOCUMENT BUTTONS
    # --------------------------------------------------------

    from plugins.callbacks import (
        show_format_buttons
    )

    await show_format_buttons(
        message,
        url
    )
