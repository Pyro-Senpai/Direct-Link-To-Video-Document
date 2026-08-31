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


# Current auto-delete time in seconds
auto_delete_seconds = DEFAULT_AUTO_DELETE


# ============================================================
# PARSE TIME
# ============================================================

def parse_time(value: str):

    value = value.lower().strip()

    if value == "off":
        return 0

    # Examples:
    # 30
    # 30s
    # 5m
    # 2h
    # 1d

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


# ============================================================
# FORMAT TIME
# ============================================================

def format_delete_time(seconds):

    if seconds <= 0:
        return "OFF"

    if seconds < 60:
        return f"{seconds} seconds"

    if seconds < 3600:
        minutes = seconds // 60
        remaining = seconds % 60

        if remaining:
            return (
                f"{minutes} minutes "
                f"{remaining} seconds"
            )

        return f"{minutes} minutes"

    if seconds < 86400:
        hours = seconds // 3600
        remaining = seconds % 3600
        minutes = remaining // 60

        if minutes:
            return (
                f"{hours} hours "
                f"{minutes} minutes"
            )

        return f"{hours} hours"

    days = seconds // 86400
    return f"{days} days"


# ============================================================
# ADMIN CHECK
# ============================================================

def is_admin(user_id):

    return (
        ADMIN_ID != 0
        and user_id == ADMIN_ID
    )


# ============================================================
# SET AUTO DELETE
# ============================================================

@Client.on_message(
    filters.command("setdelete")
    & filters.private
)
async def set_delete_command(
    client: Client,
    message: Message,
):

    global auto_delete_seconds

    # --------------------------------------------------------
    # ADMIN ONLY
    # --------------------------------------------------------

    if not is_admin(
        message.from_user.id
    ):

        await message.reply_text(
            "❌ **Admin only command.**"
        )

        return

    # --------------------------------------------------------
    # ARGUMENT
    # --------------------------------------------------------

    if len(message.command) < 2:

        current = format_delete_time(
            auto_delete_seconds
        )

        await message.reply_text(
            "⚙️ **Auto Delete Settings**\n\n"
            f"🗑️ Current: `{current}`\n\n"
            "**Examples:**\n"
            "`/setdelete 30` → 30 seconds\n"
            "`/setdelete 5m` → 5 minutes\n"
            "`/setdelete 2h` → 2 hours\n"
            "`/setdelete 1d` → 1 day\n"
            "`/setdelete off` → Disable"
        )

        return

    value = message.command[1]

    seconds = parse_time(
        value
    )

    if seconds is None:

        await message.reply_text(
            "❌ **Invalid time.**\n\n"
            "Examples:\n"
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
            "🗑️ **Auto-delete disabled.**"
        )

        return

    await message.reply_text(
        "✅ **Auto-delete updated.**\n\n"
        f"⏱️ Delete after: "
        f"`{format_delete_time(seconds)}`"
    )


# ============================================================
# GET CURRENT SETTING
# ============================================================

@Client.on_message(
    filters.command("delete")
    & filters.private
)
async def delete_status(
    client: Client,
    message: Message,
):

    if not is_admin(
        message.from_user.id
    ):

        await message.reply_text(
            "❌ **Admin only command.**"
        )

        return

    await message.reply_text(
        "🗑️ **Auto Delete**\n\n"
        f"⏱️ Current setting: "
        f"`{format_delete_time(auto_delete_seconds)}`"
    )


# ============================================================
# SCHEDULE MESSAGE DELETE
# ============================================================

async def schedule_delete(
    client,
    chat_id,
    message_id,
):

    if auto_delete_seconds <= 0:
        return

    try:

        await asyncio.sleep(
            auto_delete_seconds
        )

        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_id
        )

        logger.info(
            "Auto-deleted message %s "
            "from chat %s",
            message_id,
            chat_id
        )

    except asyncio.CancelledError:

        pass

    except Exception:

        logger.exception(
            "Auto-delete failed"
        )
