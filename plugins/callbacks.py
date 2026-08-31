# plugins/callbacks.py

import uuid
import logging

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from plugins.downloader import (
    start_download
)


logger = logging.getLogger(__name__)


# ============================================================
# Pending Downloads
# ============================================================

# {
#     "short_id": {
#         "user_id": 123456,
#         "url": "https://example.com/video.mp4"
#     }
# }

pending_downloads = {}


# ============================================================
# Create Download Request
# ============================================================

def create_download_request(
    user_id: int,
    url: str
) -> str:

    short_id = uuid.uuid4().hex[:12]

    pending_downloads[short_id] = {
        "user_id": user_id,
        "url": url
    }

    return short_id


# ============================================================
# Get Download Request
# ============================================================

def get_download_request(
    short_id: str
):

    return pending_downloads.get(
        short_id
    )


# ============================================================
# Delete Download Request
# ============================================================

def delete_download_request(
    short_id: str
):

    pending_downloads.pop(
        short_id,
        None
    )


# ============================================================
# Video / Document Buttons
# ============================================================

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
            "❌ Invalid request.",
            show_alert=True
        )

        return


    # --------------------------------------------------------
    # Get stored URL
    # --------------------------------------------------------

    request = get_download_request(
        short_id
    )

    if not request:

        await callback_query.answer(
            "❌ This download request has expired.",
            show_alert=True
        )

        return


    # --------------------------------------------------------
    # Security check
    # --------------------------------------------------------

    if request["user_id"] != user_id:

        await callback_query.answer(
            "❌ This button belongs to another user.",
            show_alert=True
        )

        return


    url = request["url"]


    # --------------------------------------------------------
    # Remove request
    # --------------------------------------------------------

    delete_download_request(
        short_id
    )


    await callback_query.answer()


    # --------------------------------------------------------
    # Start download
    # --------------------------------------------------------

    await start_download(
        client=client,
        message=callback_query.message,
        user_id=user_id,
        url=url,
        mode=mode
    )


# ============================================================
# Cancel Button
# ============================================================

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
        "❌ Cancelled."
    )

    # Import here to avoid circular imports
    from plugins.downloader import (
        cancel_download
    )

    cancelled = await cancel_download(
        user_id
    )

    if cancelled:

        try:
            await callback_query.message.edit_text(
                "❌ **Download cancelled.**"
            )
        except Exception:
            pass

    else:

        try:
            await callback_query.message.edit_text(
                "ℹ️ **No active download.**"
            )
        except Exception:
            pass
