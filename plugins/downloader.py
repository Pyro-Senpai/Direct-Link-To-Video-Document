import uuid
import time
import logging

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)

from plugins.downloader import (
    start_download,
    cancel_download,
    active_downloads,
    download_status,
    upload_status,
)

logger = logging.getLogger(__name__)

pending_downloads = {}


def create_download_request(
    user_id: int,
    url: str
) -> str:

    short_id = uuid.uuid4().hex[:12]

    pending_downloads[short_id] = {
        "user_id": user_id,
        "url": url,
    }

    return short_id


def get_download_request(
    short_id: str
):

    return pending_downloads.get(
        short_id
    )


def delete_download_request(
    short_id: str
):

    pending_downloads.pop(
        short_id,
        None
    )


def format_keyboard(
    short_id: str
):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Video",
                    callback_data=f"video:{short_id}"
                ),
                InlineKeyboardButton(
                    "📄 Document",
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


def progress_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="refresh_download"
                ),
                InlineKeyboardButton(
                    "❌ Cancel",
                    callback_data="cancel_download"
                )
            ]
        ]
    )


async def show_format_buttons(
    message: Message,
    url: str
):

    if not message.from_user:
        return

    short_id = create_download_request(
        user_id=message.from_user.id,
        url=url
    )

    await message.reply_text(
        "📥 **Choose download format:**",
        reply_markup=format_keyboard(
            short_id
        )
    )


@Client.on_callback_query(
    filters.regex(
        r"^(video|document):"
    )
)
async def format_callback(
    client: Client,
    callback_query: CallbackQuery
):

    user_id = callback_query.from_user.id
    data = callback_query.data

    try:

        mode, short_id = data.split(
            ":",
            1
        )

    except ValueError:

        await callback_query.answer(
            "Invalid request.",
            show_alert=True
        )

        return

    request = get_download_request(
        short_id
    )

    if not request:

        await callback_query.answer(
            "This request has expired.",
            show_alert=True
        )

        return

    if request["user_id"] != user_id:

        await callback_query.answer(
            "This button belongs to another user.",
            show_alert=True
        )

        return

    url = request["url"]

    delete_download_request(
        short_id
    )

    await callback_query.answer(
        "Starting..."
    )

    await start_download(
        client=client,
        message=callback_query.message,
        user_id=user_id,
        url=url,
        mode=mode
    )


@Client.on_callback_query(
    filters.regex(
        r"^refresh_download$"
    )
)
async def refresh_callback(
    client: Client,
    callback_query: CallbackQuery
):

    user_id = callback_query.from_user.id

    download = active_downloads.get(
        user_id
    )

    if not download:

        await callback_query.answer(
            "No active download.",
            show_alert=True
        )

        return

    phase = download.get(
        "phase",
        "download"
    )

    try:

        if phase == "download":

            current = download.get(
                "downloaded",
                0
            )

            total = download.get(
                "total",
                0
            )

            start_time = download.get(
                "start_time",
                time.time()
            )

            text = download_status(
                current,
                total,
                start_time
            )

        elif phase == "upload":

            current = download.get(
                "uploaded",
                0
            )

            total = download.get(
                "upload_total",
                0
            )

            start_time = download.get(
                "upload_start"
            )

            if not start_time:
                start_time = time.time()

            text = upload_status(
                current,
                total,
                start_time
            )

        else:

            text = (
                "🔍 **Checking link...**"
            )

        await callback_query.message.edit_text(
            text,
            reply_markup=progress_keyboard()
        )

        await callback_query.answer(
            "🔄 Refreshed"
        )

    except Exception as error:

        logger.warning(
            "Refresh failed: %s",
            error
        )

        await callback_query.answer(
            "Unable to refresh.",
            show_alert=True
        )


@Client.on_callback_query(
    filters.regex(
        r"^cancel_download$"
    )
)
async def cancel_callback(
    client: Client,
    callback_query: CallbackQuery
):

    user_id = callback_query.from_user.id

    await callback_query.answer(
        "❌ Cancelling..."
    )

    cancelled = await cancel_download(
        user_id
    )

    if cancelled:

        try:

            await callback_query.message.edit_text(
                "❌ **Download cancelled.**"
            )

        except Exception as error:

            logger.warning(
                "Failed to edit cancel message: %s",
                error
            )

    else:

        try:

            await callback_query.message.edit_text(
                "ℹ️ **No active download.**"
            )

        except Exception as error:

            logger.warning(
                "Failed to edit cancel message: %s",
                error
            )


@Client.on_callback_query(
    filters.regex(
        r"^close_start$"
    )
)
async def close_start_callback(
    client: Client,
    callback_query: CallbackQuery
):

    await callback_query.answer()

    try:

        await callback_query.message.delete()

    except Exception as error:

        logger.warning(
            "Failed to close start message: %s",
            error
        )


@Client.on_callback_query(
    filters.regex(
        r"^close_help$"
    )
)
async def close_help_callback(
    client: Client,
    callback_query: CallbackQuery
):

    await callback_query.answer()

    try:

        await callback_query.message.delete()

    except Exception as error:

        logger.warning(
            "Failed to close help message: %s",
            error
        )


@Client.on_callback_query(
    filters.regex(
        r"^close_about$"
    )
)
async def close_about_callback(
    client: Client,
    callback_query: CallbackQuery
):

    await callback_query.answer()

    try:

        await callback_query.message.delete()

    except Exception as error:

        logger.warning(
            "Failed to close about message: %s",
            error
        )


@Client.on_callback_query(
    filters.regex(
        r"^back_start$"
    )
)
async def back_start_callback(
    client: Client,
    callback_query: CallbackQuery
):

    await callback_query.answer()

    try:

        await callback_query.message.delete()

    except Exception as error:

        logger.warning(
            "Failed to go back: %s",
            error
        )
