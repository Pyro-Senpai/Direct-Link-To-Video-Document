import os
import re
import time
import asyncio
import logging
from urllib.parse import urlparse, unquote

import aiohttp
from pyrogram import Client
from pyrogram.types import Message

from config import (
    DOWNLOAD_DIR,
    MAX_FILE_SIZE,
    DEFAULT_CAPTION,
)

from database.database import save_download


logger = logging.getLogger(__name__)


# ============================================================
# Active Downloads
# ============================================================

active_downloads = {}


# ============================================================
# Constants
# ============================================================

CHUNK_SIZE = 1024 * 1024  # 1 MB
PROGRESS_INTERVAL = 3


# ============================================================
# Format Bytes
# ============================================================

def format_bytes(size: int) -> str:

    if size <= 0:
        return "0 B"

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    size = float(size)
    index = 0

    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1

    return f"{size:.2f} {units[index]}"


# ============================================================
# Format Time
# ============================================================

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


# ============================================================
# Safe Filename
# ============================================================

def safe_filename(filename: str) -> str:

    filename = unquote(filename)

    filename = os.path.basename(filename)

    filename = re.sub(
        r'[<>:"/\\|?*\x00-\x1F]',
        "_",
        filename,
    )

    filename = filename.strip(" .")

    if not filename:
        filename = "downloaded_file"

    return filename[:200]


# ============================================================
# Filename From URL
# ============================================================

def filename_from_url(url: str) -> str:

    try:

        parsed = urlparse(url)

        filename = os.path.basename(
            parsed.path.rstrip("/")
        )

        if filename:
            return safe_filename(filename)

    except Exception:
        pass

    return "downloaded_file"


# ============================================================
# Progress Text
# ============================================================

def make_progress_text(
    current: int,
    total: int,
    start_time: float,
) -> str:

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
            bar_length
            * current
            / total
        )

        filled = min(
            filled,
            bar_length
        )

        bar = (
            "█" * filled
            + "░" * (bar_length - filled)
        )

        return (
            "📥 **Downloading...**\n\n"
            f"`{bar}` **{percentage:.1f}%**\n\n"
            f"📦 `{format_bytes(current)}` / "
            f"`{format_bytes(total)}`\n"
            f"⚡ `{format_bytes(speed)}/s`\n"
            f"⏱ `{format_time(eta)}`"
        )

    return (
        "📥 **Downloading...**\n\n"
        f"📦 `{format_bytes(current)}`\n"
        f"⚡ `{format_bytes(speed)}/s`"
    )


# ============================================================
# Update Progress
# ============================================================

async def update_progress(
    message: Message,
    current: int,
    total: int,
    start_time: float,
):

    try:

        text = make_progress_text(
            current=current,
            total=total,
            start_time=start_time,
        )

        await message.edit_text(text)

    except Exception:
        pass


# ============================================================
# Download File
# ============================================================

async def download_file(
    url: str,
    filepath: str,
    status_message: Message,
    user_id: int,
) -> int:

    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=30,
        sock_read=120,
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        ),
        "Accept": "*/*",
    }

    downloaded = 0
    total_size = 0

    start_time = time.time()
    last_update = 0

    async with aiohttp.ClientSession(
        timeout=timeout,
        headers=headers,
    ) as session:

        async with session.get(
            url,
            allow_redirects=True,
        ) as response:

            if response.status != 200:

                raise RuntimeError(
                    f"HTTP error: {response.status}"
                )

            # ------------------------------------------------
            # Content Length
            # ------------------------------------------------

            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length:

                try:
                    total_size = int(content_length)

                except (ValueError, TypeError):
                    total_size = 0

            # ------------------------------------------------
            # Check 4 GB limit before download
            # ------------------------------------------------

            if total_size > MAX_FILE_SIZE:

                raise RuntimeError(
                    "The file is larger than the "
                    "4 GB download limit."
                )

            # ------------------------------------------------
            # Download
            # ------------------------------------------------

            with open(
                filepath,
                "wb",
            ) as output:

                async for chunk in response.content.iter_chunked(
                    CHUNK_SIZE
                ):

                    # Check cancellation
                    if user_id not in active_downloads:

                        raise asyncio.CancelledError

                    if not chunk:
                        continue

                    downloaded += len(chunk)

                    # ------------------------------------------------
                    # Check actual downloaded size
                    # ------------------------------------------------

                    if downloaded > MAX_FILE_SIZE:

                        raise RuntimeError(
                            "The file exceeded the "
                            "4 GB download limit."
                        )

                    output.write(chunk)

                    # ------------------------------------------------
                    # Progress update
                    # ------------------------------------------------

                    now = time.time()

                    if (
                        now - last_update
                        >= PROGRESS_INTERVAL
                    ):

                        await update_progress(
                            message=status_message,
                            current=downloaded,
                            total=total_size,
                            start_time=start_time,
                        )

                        last_update = now

    return downloaded


# ============================================================
# Start Download
# ============================================================

async def start_download(
    client: Client,
    message: Message,
    user_id: int,
    url: str,
    mode: str,
):

    # --------------------------------------------------------
    # Prevent multiple downloads
    # --------------------------------------------------------

    if user_id in active_downloads:

        try:

            await message.edit_text(
                "⚠️ **You already have a download running.**\n\n"
                "Use `/cancel` to stop it first."
            )

        except Exception:
            pass

        return

    # --------------------------------------------------------
    # Validate mode
    # --------------------------------------------------------

    if mode not in (
        "video",
        "document",
    ):

        try:

            await message.edit_text(
                "❌ **Invalid file type.**"
            )

        except Exception:
            pass

        return

    # --------------------------------------------------------
    # Create filename
    # --------------------------------------------------------

    filename = filename_from_url(url)

    timestamp = int(
        time.time()
    )

    filepath = os.path.join(
        DOWNLOAD_DIR,
        f"{user_id}_{timestamp}_{filename}",
    )

    # --------------------------------------------------------
    # Register active download
    # --------------------------------------------------------

    active_downloads[user_id] = {
        "url": url,
        "filepath": filepath,
        "mode": mode,
        "started_at": time.time(),
    }

    try:

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "🔍 **Checking download link...**"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        downloaded = await download_file(
            url=url,
            filepath=filepath,
            status_message=message,
            user_id=user_id,
        )

        # ----------------------------------------------------
        # Make sure file exists
        # ----------------------------------------------------

        if not os.path.exists(filepath):

            raise RuntimeError(
                "Downloaded file was not created."
            )

        actual_size = os.path.getsize(
            filepath
        )

        if actual_size <= 0:

            raise RuntimeError(
                "Downloaded file is empty."
            )

        if actual_size > MAX_FILE_SIZE:

            raise RuntimeError(
                "Downloaded file exceeded "
                "the 4 GB limit."
            )

        # ----------------------------------------------------
        # Upload status
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "📤 **Uploading to Telegram...**\n\n"
                f"📦 `{format_bytes(actual_size)}`"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Caption
        # ----------------------------------------------------

        caption = DEFAULT_CAPTION

        # ----------------------------------------------------
        # Upload as Video
        # ----------------------------------------------------

        if mode == "video":

            await client.send_video(
                chat_id=user_id,
                video=filepath,
                caption=caption,
                supports_streaming=True,
            )

        # ----------------------------------------------------
        # Upload as Document
        # ----------------------------------------------------

        elif mode == "document":

            await client.send_document(
                chat_id=user_id,
                document=filepath,
                caption=caption,
            )

        # ----------------------------------------------------
        # Save history
        # ----------------------------------------------------

        try:

            await save_download(
                user_id=user_id,
                url=url,
                filename=filename,
                file_type=mode,
                file_size=actual_size,
            )

        except Exception:

            logger.exception(
                "Failed to save download history."
            )

        # ----------------------------------------------------
        # Finished
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "✅ **Download completed!**\n\n"
                f"📦 `{format_bytes(actual_size)}`\n"
                f"📁 `{mode}`"
            )

        except Exception:
            pass

        # Give Telegram a moment before deleting status
        await asyncio.sleep(2)

        try:
            await message.delete()
        except Exception:
            pass

    except asyncio.CancelledError:

        logger.info(
            "Download cancelled by user: %s",
            user_id,
        )

        try:

            await message.edit_text(
                "❌ **Download cancelled.**"
            )

        except Exception:
            pass

    except aiohttp.ClientError as e:

        logger.error(
            "HTTP download error: %s",
            e,
        )

        try:

            await message.edit_text(
                "❌ **Download failed.**\n\n"
                "Could not connect to the download server."
            )

        except Exception:
            pass

    except Exception as e:

        logger.exception(
            "Download failed for user %s",
            user_id,
        )

        error_text = str(e)

        if len(error_text) > 800:
            error_text = error_text[:800] + "..."

        try:

            await message.edit_text(
                "❌ **Download failed.**\n\n"
                f"`{error_text}`"
            )

        except Exception:
            pass

    finally:

        # ----------------------------------------------------
        # Remove active task
        # ----------------------------------------------------

        active_downloads.pop(
            user_id,
            None,
        )

        # ----------------------------------------------------
        # Delete temporary file
        # ----------------------------------------------------

        if os.path.exists(filepath):

            try:

                os.remove(filepath)

                logger.info(
                    "Deleted temporary file: %s",
                    filepath,
                )

            except Exception:

                logger.exception(
                    "Failed to delete temporary file: %s",
                    filepath,
                )


# ============================================================
# Cancel Download
# ============================================================

async def cancel_download(
    user_id: int,
) -> bool:

    download = active_downloads.get(
        user_id
    )

    if not download:

        return False

    # Removing the user from active_downloads causes
    # download_file() to raise asyncio.CancelledError
    # on its next chunk.

    active_downloads.pop(
        user_id,
        None,
    )

    filepath = download.get(
        "filepath"
    )

    # --------------------------------------------------------
    # Try immediate cleanup
    # --------------------------------------------------------

    if filepath and os.path.exists(filepath):

        try:

            os.remove(filepath)

        except Exception:

            logger.exception(
                "Failed to remove cancelled file."
            )

    return True
