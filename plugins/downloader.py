# plugins/downloader.py

import os
import re
import time
import asyncio
import aiohttp

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from config import (
    DOWNLOAD_DIR,
    MAX_FILE_SIZE,
    DEFAULT_CAPTION
)

from database.database import (
    add_user,
    save_download
)


# ============================================================
# Active Downloads
# ============================================================

active_downloads = {}


# ============================================================
# URL Pattern
# ============================================================

URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE
)


# ============================================================
# Helpers
# ============================================================

def format_bytes(size: int) -> str:

    if size <= 0:
        return "0 B"

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    index = 0
    size = float(size)

    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1

    return f"{size:.2f} {units[index]}"


def format_time(seconds: float) -> str:

    if seconds <= 0:
        return "0s"

    seconds = int(seconds)

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    if days:
        return f"{days}d {hours}h"

    if hours:
        return f"{hours}h {minutes}m"

    if minutes:
        return f"{minutes}m {seconds}s"

    return f"{seconds}s"


def safe_filename(filename: str) -> str:

    filename = os.path.basename(filename)

    filename = re.sub(
        r'[<>:"/\\|?*\x00-\x1F]',
        "_",
        filename
    )

    filename = filename.strip(" .")

    if not filename:
        filename = "downloaded_file"

    return filename[:200]


def get_filename_from_url(url: str) -> str:

    clean_url = url.split("?", 1)[0]
    clean_url = clean_url.split("#", 1)[0]

    filename = os.path.basename(
        clean_url.rstrip("/")
    )

    return safe_filename(filename)


# ============================================================
# Progress Formatter
# ============================================================

def make_progress(
    current: int,
    total: int,
    start_time: float
):

    elapsed = time.time() - start_time

    if elapsed <= 0:
        elapsed = 0.1

    speed = current / elapsed

    if total > 0:

        percentage = (
            current / total
        ) * 100

        remaining = total - current

        eta = (
            remaining / speed
            if speed > 0
            else 0
        )

        bar_length = 12

        filled = int(
            bar_length * current / total
        )

        bar = (
            "█" * filled
            + "░" * (bar_length - filled)
        )

        return (
            f"📥 **Downloading...**\n\n"
            f"`{bar}` **{percentage:.1f}%**\n\n"
            f"📦 `{format_bytes(current)}` / "
            f"`{format_bytes(total)}`\n"
            f"⚡ `{format_bytes(speed)}/s`\n"
            f"⏱ `{format_time(eta)}`"
        )

    return (
        f"📥 **Downloading...**\n\n"
        f"📦 `{format_bytes(current)}`\n"
        f"⚡ `{format_bytes(speed)}/s`"
    )


# ============================================================
# Download Function
# ============================================================

async def download_file(
    url: str,
    filepath: str,
    status_message: Message
):

    user_id = status_message.chat.id

    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=30,
        sock_read=60
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "Chrome/120 Safari/537.36"
        )
    }

    start_time = time.time()

    downloaded = 0
    total_size = 0

    last_update = 0

    async with aiohttp.ClientSession(
        timeout=timeout,
        headers=headers
    ) as session:

        async with session.get(
            url,
            allow_redirects=True
        ) as response:

            if response.status != 200:

                raise RuntimeError(
                    f"Server returned HTTP "
                    f"{response.status}"
                )

            # ------------------------------------------------
            # Content-Length
            # ------------------------------------------------

            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length:

                try:
                    total_size = int(
                        content_length
                    )

                except ValueError:
                    total_size = 0

            # ------------------------------------------------
            # Early 4 GB check
            # ------------------------------------------------

            if total_size > MAX_FILE_SIZE:

                raise RuntimeError(
                    "File is larger than the "
                    "4 GB limit."
                )

            # ------------------------------------------------
            # Download
            # ------------------------------------------------

            with open(filepath, "wb") as file:

                async for chunk in response.content.iter_chunked(
                    1024 * 1024
                ):

                    if user_id not in active_downloads:
                        raise asyncio.CancelledError

                    if not chunk:
                        continue

                    downloaded += len(chunk)

                    # Check actual downloaded size
                    if downloaded > MAX_FILE_SIZE:

                        raise RuntimeError(
                            "File exceeded the "
                            "4 GB limit."
                        )

                    file.write(chunk)

                    # ------------------------------------------------
                    # Update progress every ~3 seconds
                    # ------------------------------------------------

                    now = time.time()

                    if now - last_update >= 3:

                        text = make_progress(
                            downloaded,
                            total_size,
                            start_time
                        )

                        try:
                            await status_message.edit_text(
                                text
                            )
                        except Exception:
                            pass

                        last_update = now

    return downloaded, total_size


# ============================================================
# Detect URL
# ============================================================

@Client.on_message(
    filters.text
    & ~filters.command(
        ["start", "cancel"]
    )
)
async def detect_url(
    client: Client,
    message: Message
):

    user = message.from_user

    if not user:
        return

    match = URL_PATTERN.search(
        message.text or ""
    )

    if not match:

        await message.reply_text(
            "❌ **No valid URL found.**\n\n"
            "Please send a direct download link."
        )

        return

    url = match.group(0).rstrip(
        ".,!?)]}"
    )

    await add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🎬 Video",
                    callback_data=f"video|{url}"
                ),
                InlineKeyboardButton(
                    "📁 Document",
                    callback_data=f"document|{url}"
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
        "🔗 **Link detected!**\n\n"
        "Choose how you want me to send the file:",
        reply_markup=keyboard
    )


# ============================================================
# Callback Handler
# ============================================================

@Client.on_callback_query(
    filters.regex(
        r"^(video|document)\|"
    )
)
async def download_callback(
    client: Client,
    callback_query: CallbackQuery
):

    user = callback_query.from_user

    data = callback_query.data

    mode, url = data.split(
        "|",
        1
    )

    user_id = user.id

    if user_id in active_downloads:

        await callback_query.answer(
            "⚠️ You already have a download running.",
            show_alert=True
        )

        return

    await callback_query.answer()

    filename = get_filename_from_url(
        url
    )

    filepath = os.path.join(
        DOWNLOAD_DIR,
        f"{user_id}_{int(time.time())}_{filename}"
    )

    active_downloads[user_id] = True

    status = callback_query.message

    try:

        await status.edit_text(
            "🔍 **Checking file...**"
        )

        downloaded, total = await download_file(
            url=url,
            filepath=filepath,
            status_message=status
        )

        await status.edit_text(
            "📤 **Uploading to Telegram...**"
        )

        caption = DEFAULT_CAPTION

        if mode == "video":

            await client.send_video(
                chat_id=user_id,
                video=filepath,
                caption=caption,
                supports_streaming=True
            )

        else:

            await client.send_document(
                chat_id=user_id,
                document=filepath,
                caption=caption
            )

        # ----------------------------------------------------
        # Save history
        # ----------------------------------------------------

        await save_download(
            user_id=user_id,
            url=url,
            filename=filename,
            file_type=mode,
            file_size=downloaded
        )

        try:
            await status.delete()
        except Exception:
            pass

    except asyncio.CancelledError:

        try:
            await status.edit_text(
                "❌ **Download cancelled.**"
            )
        except Exception:
            pass

    except Exception as e:

        try:
            await status.edit_text(
                f"❌ **Download failed.**\n\n"
                f"`{str(e)[:1000]}`"
            )
        except Exception:
            pass

    finally:

        active_downloads.pop(
            user_id,
            None
        )

        if os.path.exists(filepath):

            try:
                os.remove(filepath)
            except Exception:
                pass
