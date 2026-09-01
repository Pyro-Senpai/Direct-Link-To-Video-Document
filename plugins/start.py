import re

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


@Client.on_message(
    filters.command("start")
    & filters.private
)
async def start_command(
    client: Client,
    message: Message
):

    keyboard = start_keyboard()

    if START_IMAGE:

        try:

            await message.reply_photo(
                photo=START_IMAGE,
                caption=START_TEXT,
                reply_markup=keyboard
            )

            return

        except Exception:
            pass

    await message.reply_text(
        START_TEXT,
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

    try:

        await callback_query.message.edit_text(
            START_TEXT,
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
            "❌ **Please send a valid HTTP/HTTPS URL.**"
        )

        return

    if len(
        url.encode("utf-8")
    ) > 150:

        await message.reply_text(
            "❌ **This URL is too long.**\n\n"
            "Please send a shorter direct download URL."
        )

        return

    from plugins.callbacks import (
        show_format_buttons
    )

    await show_format_buttons(
        message,
        url
    )
