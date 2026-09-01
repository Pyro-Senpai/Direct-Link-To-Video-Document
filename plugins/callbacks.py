plugins/callbacks.py

import uuid
import logging

from pyrogram import Client, filters
from pyrogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton,
CallbackQuery,
Message
)

from plugins.downloader import (
start_download
)

logger = logging.getLogger(name)

============================================================

Pending Downloads

============================================================

{

"short_id": {

"user_id": 123456,

"url": "https://example.com/video.mp4"

}

}

pending_downloads = {}

============================================================

Create Download Request

============================================================

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

============================================================

Get Download Request

============================================================

def get_download_request(
short_id: str
):

return pending_downloads.get(
    short_id
)

============================================================

Delete Download Request

============================================================

def delete_download_request(
short_id: str
):

pending_downloads.pop(
    short_id,
    None
)

============================================================

Show Video / Document Buttons

============================================================

async def show_format_buttons(
message: Message,
url: str
):

# Create a short ID instead of putting
# the full URL inside callback_data.

short_id = create_download_request(
    user_id=message.from_user.id,
    url=url
)

keyboard = InlineKeyboardMarkup(
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

await message.reply_text(
    "📥 **Choose download format:**",
    reply_markup=keyboard
)

============================================================

Video / Document Callback

============================================================

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

# --------------------------------------------------------
# Extract mode and short ID
# --------------------------------------------------------

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
# Get stored download request
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
# Security Check
# --------------------------------------------------------

if request["user_id"] != user_id:

    await callback_query.answer(
        "❌ This button belongs to another user.",
        show_alert=True
    )

    return


# --------------------------------------------------------
# Get URL
# --------------------------------------------------------

url = request["url"]


# --------------------------------------------------------
# Remove pending request
# --------------------------------------------------------

delete_download_request(
    short_id
)


# --------------------------------------------------------
# Answer Callback
# --------------------------------------------------------

await callback_query.answer(
    "📥 Starting download..."
)


# --------------------------------------------------------
# Start Download
# --------------------------------------------------------

await start_download(
    client=client,
    message=callback_query.message,
    user_id=user_id,
    url=url,
    mode=mode
)

============================================================

Cancel Button

============================================================

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


# --------------------------------------------------------
# Answer Callback
# --------------------------------------------------------

await callback_query.answer(
    "❌ Cancelled."
)


# --------------------------------------------------------
# Cancel Active Download
# --------------------------------------------------------

from plugins.downloader import (
    cancel_download
)

cancelled = await cancel_download(
    user_id
)


# --------------------------------------------------------
# Update Message
# --------------------------------------------------------

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
