import uuid
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
)

logger = logging.getLogger(__name__)

pending_downloads = {}


def create_download_request(user_id: int, url: str) -> str:
    short_id = uuid.uuid4().hex[:12]

    pending_downloads[short_id] = {
        "user_id": user_id,
        "url": url,
    }

    return short_id


def get_download_request(short_id: str):
    return pending_downloads.get(short_id)


def delete_download_request(short_id: str):
    pending_downloads.pop(short_id, None)


async def show_format_buttons(message: Message, url: str):
    if not message.from_user:
        return

    short_id = create_download_request(
        user_id=message.from_user.id,
        url=url,
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Vɪᴅᴇᴏ",
                    callback_data=f"video:{short_id}",
                ),
                InlineKeyboardButton(
                    "Dᴏᴄᴜᴍᴇɴᴛ",
                    callback_data=f"document:{short_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    "Cᴀɴᴄᴇʟ",
                    callback_data="cancel_download",
                ),
            ],
        ]
    )

    await message.reply_text(
        "**ᴄʜᴏᴏsᴇ ᴅᴏᴡɴʟᴏᴀᴅ ғᴏʀᴍᴀᴛ:**",
        reply_markup=keyboard,
    )


@Client.on_callback_query(
    filters.regex(r"^(video|document):")
)
async def format_callback(
    client: Client,
    callback_query: CallbackQuery,
):
    user_id = callback_query.from_user.id
    data = callback_query.data

    try:
        mode, short_id = data.split(":", 1)
    except ValueError:
        await callback_query.answer(
            "ɪɴᴠᴀʟɪᴅ ʀᴇǫᴜᴇsᴛ.",
            show_alert=True,
        )
        return

    request = get_download_request(short_id)

    if not request:
        await callback_query.answer(
            "ᴛʜɪs ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇǫᴜᴇsᴛ ʜᴀs ᴇxᴘᴀʀɪᴇᴅ.",
            show_alert=True,
        )
        return

    if request["user_id"] != user_id:
        await callback_query.answer(
            "ᴛʜɪs ʙᴜᴛᴛᴏɴ ʙᴇʟᴏɴɢs ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ.",
            show_alert=True,
        )
        return

    url = request["url"]

    delete_download_request(short_id)

    await callback_query.answer(
        "sᴛᴀʀᴛɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ..."
    )

    await start_download(
        client=client,
        message=callback_query.message,
        user_id=user_id,
        url=url,
        mode=mode,
    )


@Client.on_callback_query(
    filters.regex(r"^cancel_download$")
)
async def cancel_callback(
    client: Client,
    callback_query: CallbackQuery,
):
    user_id = callback_query.from_user.id

    await callback_query.answer(
        "Cᴀɴᴄᴀʟʟᴇᴅ."
    )

    cancelled = await cancel_download(user_id)

    if cancelled:
        try:
            await callback_query.message.edit_text(
                "**ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ.**"
            )
        except Exception as e:
            logger.warning(
                "ғᴀɪʟᴇᴅ ᴛᴏ ᴇᴅɪᴛ ᴄᴀɴᴄᴇʟ ᴍᴇssᴀɢᴇ: %s",
                e,
            )
    else:
        try:
            await callback_query.message.edit_text(
                "**ɴᴏ ᴀᴄᴛɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅ.**"
            )
        except Exception as e:
            logger.warning(
                "ғᴀɪʟᴇᴅ ᴛᴏ ᴇᴅɪᴛ ᴄᴀɴᴄᴇʟ ᴍᴇssᴀɢᴇ: %s",
                e,
            )
