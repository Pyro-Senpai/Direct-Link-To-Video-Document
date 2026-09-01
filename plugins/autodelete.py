import re
import asyncio
import logging

from pyrogram import Client, filters
from pyrogram.types import Message

from config import (
    ADMIN_ID,
    DEFAULT_AUTO_DELETE,
)

logger = logging.getLogger(__name__)

auto_delete_seconds = DEFAULT_AUTO_DELETE


def parse_time(value: str):

    value = value.lower().strip()

    if value == "off":
        return 0

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*(s|sec|secs|second|seconds|m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)?",
        value,
    )

    if not match:
        return None

    number = float(match.group(1))
    unit = match.group(2) or "s"

    if number <= 0:
        return None

    if unit in (
        "s",
        "sec",
        "secs",
        "second",
        "seconds",
    ):
        multiplier = 1

    elif unit in (
        "m",
        "min",
        "mins",
        "minute",
        "minutes",
    ):
        multiplier = 60

    elif unit in (
        "h",
        "hr",
        "hrs",
        "hour",
        "hours",
    ):
        multiplier = 60 * 60

    elif unit in (
        "d",
        "day",
        "days",
    ):
        multiplier = 24 * 60 * 60

    else:
        return None

    return int(number * multiplier)


def format_delete_time(seconds):

    if seconds <= 0:
        return "ᴏꜰꜰ"

    if seconds < 60:
        return f"{seconds} ꜱᴇᴄᴏɴᴅꜱ"

    if seconds < 3600:

        minutes = seconds // 60
        remaining = seconds % 60

        if remaining:
            return (
                f"{minutes} ᴍɪɴᴜᴛᴇꜱ "
                f"{remaining} ꜱᴇᴄᴏɴᴅꜱ"
            )

        return f"{minutes} ᴍɪɴᴜᴛᴇꜱ"

    if seconds < 86400:

        hours = seconds // 3600
        remaining = seconds % 3600
        minutes = remaining // 60

        if minutes:
            return (
                f"{hours} ʜᴏᴜʀꜱ "
                f"{minutes} ᴍɪɴᴜᴛᴇꜱ"
            )

        return f"{hours} ʜᴏᴜʀꜱ"

    days = seconds // 86400

    return f"{days} ᴅᴀʏꜱ"


def is_admin(user_id):

    return (
        ADMIN_ID != 0
        and user_id == ADMIN_ID
    )


@Client.on_message(
    filters.command("setdelete")
    & filters.private
)
async def set_delete_command(
    client: Client,
    message: Message,
):

    global auto_delete_seconds

    if not message.from_user:
        return

    if not is_admin(
        message.from_user.id
    ):

        await message.reply_text(
            "**ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.**"
        )

        return

    if len(message.command) < 2:

        current = format_delete_time(
            auto_delete_seconds
        )

        await message.reply_text(
            "**ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ꜱᴇᴛᴛɪɴɢꜱ**\n"
            f"ᴄᴜʀʀᴇɴᴛ: `{current}`\n"
            "**ᴇxᴀᴍᴘʟᴇꜱ:**\n"
            "`/setdelete 30` → 30 seconds\n"
            "`/setdelete 5m` → 5 minutes\n"
            "`/setdelete 2h` → 2 hours\n"
            "`/setdelete 1d` → 1 day\n"
            "`/setdelete off` → Disable"
        )

        return

    value = message.command[1]

    seconds = parse_time(value)

    if seconds is None:

        await message.reply_text(
            "**ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ.**\n"
            "ᴇxᴀᴍᴘʟᴇꜱ:\n"
            "`/setdelete 30`\n"
            "`/setdelete 5m`\n"
            "`/setdelete 2h`\n"
            "`/setdelete 1d`\n"
            "`/setdelete off`"
        )

        return

    auto_delete_seconds = seconds

    if seconds == 0:

        await message.reply_text(
            "**ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴅɪꜱᴀʙʟᴇᴅ.**"
        )

        return

    await message.reply_text(
        "**ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴜᴘᴅᴀᴛᴇᴅ.**\n"
        f"ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ: "
        f"`{format_delete_time(seconds)}`"
    )


@Client.on_message(
    filters.command("delete")
    & filters.private
)
async def delete_status(
    client: Client,
    message: Message,
):

    if not message.from_user:
        return

    if not is_admin(
        message.from_user.id
    ):

        await message.reply_text(
            "**ᴀᴅᴍɪɴ ᴏɴʟʏ ᴄᴏᴍᴍᴀɴᴅ.**"
        )

        return

    await message.reply_text(
        "**ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ**\n"
        f"ᴄᴜʀʀᴇɴᴛ ꜱᴇᴛᴛɪɴɢ: "
        f"`{format_delete_time(auto_delete_seconds)}`"
    )


async def schedule_delete(
    client,
    chat_id,
    message_id,
):

    if auto_delete_seconds <= 0:
        return

    delete_after = format_delete_time(
        auto_delete_seconds
    )

    try:

        notice_message = await client.send_message(
            chat_id=chat_id,
            text=(
                "<blockquote>ʏᴏᴜʀ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ "
                f"ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴀꜰᴛᴇʀ "
                f"`{delete_after}`ᴅᴜᴇ ᴛᴏ ᴄᴏᴘʏʀɪɢʜᴛ.\n"
                "ᴘʟᴇᴀꜱᴇ ꜱᴀᴠᴇ ᴛʜᴇ ꜰɪʟᴇ ʙᴇꜰᴏʀᴇ "
                "ᴛʜᴇ ᴛɪᴍᴇʀ ᴇxᴘɪʀᴇꜱ.</blockquote>"
            )
        )

        await asyncio.sleep(
            auto_delete_seconds
        )

        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_id,
        )

        logger.info(
            "Auto-deleted message %s "
            "from chat %s",
            message_id,
            chat_id,
        )

        try:

            await notice_message.edit_text(
                "**ꜰɪʟᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**\n"
                f"ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ: "
                f"`{delete_after}`"
            )

        except Exception:

            try:

                await client.send_message(
                    chat_id=chat_id,
                    text=(
                        "**ꜰɪʟᴇ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ.**\n"
                        "ᴛʜᴇ ꜰɪʟᴇ ʜᴀꜱ ʙᴇᴇɴ "
                        "ʀᴇᴍᴏᴠᴇᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ."
                    )
                )

            except Exception:

                pass

    except asyncio.CancelledError:

        pass

    except Exception:

        logger.exception(
            "ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ғᴀɪʟᴇᴅ"
        )
