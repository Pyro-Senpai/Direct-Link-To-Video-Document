import re
import asyncio

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from config import (
    START_IMAGE,
    START_TEXT,
    HELP_TEXT,
    ABOUT_TEXT,
)

temp_msg = await message.reply("ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ . . .")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("?!")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("..")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("#?!")

    try:
        await temp_msg.delete()
    except Exception:
        pass

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
            ],
            [
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )


# ============================================================
# INFO KEYBOARD
# ============================================================

def info_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⬅️ Back",
                    callback_data="start"
                ),
                InlineKeyboardButton(
                    "❌ Close",
                    callback_data="close"
                )
            ]
        ]
    )


# ============================================================
# /START COMMAND
# ============================================================

@Client.on_message(
    filters.command("start")
    & filters.private
)
async def start_command(
    client: Client,
    message: Message
):

    user = message.from_user

    # Format start message
    try:
        formatted_text = START_TEXT.format(
            first_name=user.first_name or "",
            firstname=user.first_name or "",
            last_name=user.last_name or "",
            lastname=user.last_name or "",
            mention=user.mention
        )

    except KeyError:
        formatted_text = START_TEXT

    keyboard = start_keyboard()

    # Send image if configured
    if START_IMAGE:

        try:
            await message.reply_photo(
                photo=START_IMAGE,
                caption=formatted_text,
                reply_markup=keyboard
            )

            return

        except Exception:
            pass

    # Send normal text if image fails/not configured
    await message.reply_text(
        formatted_text,
        reply_markup=keyboard
    )


# ============================================================
# HELP CALLBACK
# ============================================================

@Client.on_callback_query(
    filters.regex(r"^help$")
)
async def help_callback(
    client: Client,
    callback_query: CallbackQuery
):

    try:
        await callback_query.message.edit_text(
            HELP_TEXT,
            reply_markup=info_keyboard()
        )

    except Exception:
        pass

    await callback_query.answer()


# ============================================================
# ABOUT CALLBACK
# ============================================================

@Client.on_callback_query(
    filters.regex(r"^about$")
)
async def about_callback(
    client: Client,
    callback_query: CallbackQuery
):

    try:
        await callback_query.message.edit_text(
            ABOUT_TEXT,
            reply_markup=info_keyboard()
        )

    except Exception:
        pass

    await callback_query.answer()


# ============================================================
# BACK TO START CALLBACK
# ============================================================

@Client.on_callback_query(
    filters.regex(r"^start$")
)
async def back_to_start(
    client: Client,
    callback_query: CallbackQuery
):

    user = callback_query.from_user

    # Format start message
    try:
        formatted_text = START_TEXT.format(
            first_name=user.first_name or "",
            firstname=user.first_name or "",
            last_name=user.last_name or "",
            lastname=user.last_name or "",
            mention=user.mention
        )

    except KeyError:
        formatted_text = START_TEXT

    try:
        await callback_query.message.edit_text(
            formatted_text,
            reply_markup=start_keyboard()
        )

    except Exception:
        pass

    await callback_query.answer()


# ============================================================
# CLOSE CALLBACK
# ============================================================

@Client.on_callback_query(
    filters.regex(r"^close$")
)
async def close_callback(
    client: Client,
    callback_query: CallbackQuery
):

    await callback_query.answer(
        "Closed."
    )

    try:
        await callback_query.message.delete()

    except Exception:
        pass


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
    # URL VALIDATION
    # --------------------------------------------------------

    if not re.match(
        r"^https?://",
        url,
        re.IGNORECASE
    ):

        await message.reply_text(
            "❌ Please send a valid HTTP/HTTPS URL."
        )

        return

    # --------------------------------------------------------
    # URL LENGTH CHECK
    # --------------------------------------------------------

    if len(
        url.encode("utf-8")
    ) > 150:

        await message.reply_text(
            "❌ This URL is too long.\n\n"
            "Please send a shorter direct download URL."
        )

        return

    # --------------------------------------------------------
    # LOADING ANIMATION
    # --------------------------------------------------------

    temp_msg = await message.reply(
        "ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ . . ."
    )

    await asyncio.sleep(0.5)

    try:
        await temp_msg.edit_text("?!")
    except Exception:
        pass

    await asyncio.sleep(0.5)

    try:
        await temp_msg.edit_text("..")
    except Exception:
        pass

    await asyncio.sleep(0.5)

    try:
        await temp_msg.edit_text("#?!")
    except Exception:
        pass

    # --------------------------------------------------------
    # DELETE LOADING MESSAGE
    # --------------------------------------------------------

    try:
        await temp_msg.delete()

    except Exception:
        pass

    # --------------------------------------------------------
    # SHOW FORMAT BUTTONS
    # --------------------------------------------------------

    from plugins.callbacks import show_format_buttons

    await show_format_buttons(
        message,
        url
    )
