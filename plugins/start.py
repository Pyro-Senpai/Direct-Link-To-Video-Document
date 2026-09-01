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

def start_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Hᴇʟᴘ",
                    callback_data="help"
                ),
                InlineKeyboardButton(
                    "Aʙᴏᴜᴛ",
                    callback_data="about"
                )
            ],
            [
                InlineKeyboardButton(
                    "Cʟᴏsᴇ",
                    callback_data="close"
                )
            ]
        ]
    )

def info_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Bᴀᴄᴋ",
                    callback_data="start"
                ),
                InlineKeyboardButton(
                    "Cʟᴏsᴇ",
                    callback_data="close"
                )
            ]
        ]
    )

@Client.on_message(
    filters.command("start")
    & filters.private
)
async def start_command(
    client: Client,
    message: Message
):
    temp_msg = await message.reply("<b>ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ . . .</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>?!</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>..</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>?!</b>")

    try:
        await temp_msg.delete()
    except Exception:
        pass

    user = message.from_user

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

    await message.reply_text(
        formatted_text,
        reply_markup=keyboard
    )

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

@Client.on_callback_query(
    filters.regex(r"^start$")
)
async def back_to_start(
    client: Client,
    callback_query: CallbackQuery
):
    user = callback_query.from_user

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

    if not re.match(
        r"^https?://",
        url,
        re.IGNORECASE
    ):
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ ʜᴛᴛᴘ/ʜᴛᴛᴘs ᴜʀʟ."
        )
        return

    if len(
        url.encode("utf-8")
    ) > 500:
        await message.reply_text(
            "Tʜɪs ᴜʀʟ ɪs ᴛᴏᴏ ʟᴏɴɢ.\n"
            "Pʟᴇᴀsᴇ sᴇɴᴅ ᴀ sʜᴏʀᴛᴇʀ ᴅɪʀᴇᴄᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴜʀʟ."
        )
        return

    temp_msg = await message.reply("<b>ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ . . .</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>?!</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>..</b>")
    await asyncio.sleep(0.5)
    await temp_msg.edit_text("<b>?!</b>")

    try:
        await temp_msg.delete()
    except Exception:
        pass

    from plugins.callbacks import show_format_buttons

    await show_format_buttons(
        message,
        url
    )
