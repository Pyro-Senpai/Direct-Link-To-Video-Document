# plugins/downloader.py

import os
import re
import time
import asyncio
import logging
import subprocess
import json

import aiohttp

from urllib.parse import urlparse, unquote

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
# ACTIVE DOWNLOADS
# ============================================================

active_downloads = {}


# ============================================================
# SETTINGS
# ============================================================

CHUNK_SIZE = 1024 * 1024
PROGRESS_INTERVAL = 3


# ============================================================
# FORMAT BYTES
# ============================================================

def format_bytes(size):

    if not size or size <= 0:
        return "0 B"

    size = float(size)

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    index = 0

    while (
        size >= 1024
        and index < len(units) - 1
    ):
        size /= 1024
        index += 1

    return f"{size:.2f} {units[index]}"


# ============================================================
# FORMAT TIME
# ============================================================

def format_time(seconds):

    if seconds is None or seconds <= 0:
        return "00:00"

    seconds = int(seconds)

    hours, remainder = divmod(
        seconds,
        3600,
    )

    minutes, seconds = divmod(
        remainder,
        60,
    )

    if hours:
        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    return (
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


# ============================================================
# SAFE FILENAME
# ============================================================

def safe_filename(filename):

    filename = unquote(
        filename
    )

    filename = os.path.basename(
        filename
    )

    filename = re.sub(
        r'[<>:"/\\|?*\x00-\x1F]',
        "_",
        filename,
    )

    filename = filename.strip(
        " ."
    )

    if not filename:
        filename = "downloaded_file"

    return filename[:200]


# ============================================================
# GET FILENAME FROM URL
# ============================================================

def filename_from_url(url):

    try:

        parsed = urlparse(url)

        filename = os.path.basename(
            parsed.path.rstrip("/")
        )

        if filename:
            return safe_filename(
                filename
            )

    except Exception:
        pass

    return "downloaded_file"


# ============================================================
# PROGRESS BAR
# ============================================================

def progress_bar(
    current,
    total,
    length=12,
):

    if total <= 0:
        return "○" * length

    percentage = (
        current / total
    )

    filled = int(
        percentage * length
    )

    filled = max(
        0,
        min(
            filled,
            length,
        ),
    )

    return (
        "●" * filled
        + "○" * (
            length - filled
        )
    )


# ============================================================
# DOWNLOAD STATUS
# ============================================================

def download_status(
    current,
    total,
    start_time,
):

    elapsed = (
        time.time()
        - start_time
    )

    if elapsed <= 0:
        elapsed = 0.1

    speed = (
        current / elapsed
    )

    if total > 0:

        percentage = (
            current / total
        ) * 100

        remaining = (
            total - current
        )

        eta = (
            remaining / speed
            if speed > 0
            else 0
        )

        bar = progress_bar(
            current,
            total,
        )

        return (
            "📥 **Mode:** `Download`\n\n"
            f"`{bar}` **{percentage:.1f}%**\n\n"
            f"📦 **File Size:** "
            f"`{format_bytes(current)}` / "
            f"`{format_bytes(total)}`\n"
            f"🚀 **Speed:** "
            f"`{format_bytes(speed)}/s`\n"
            f"⏳ **ETA:** "
            f"`{format_time(eta)}`"
        )

    return (
        "📥 **Mode:** `Download`\n\n"
        f"📦 **File Size:** "
        f"`{format_bytes(current)}`\n"
        f"🚀 **Speed:** "
        f"`{format_bytes(speed)}/s`\n"
        "⏳ **ETA:** `Calculating...`"
    )


# ============================================================
# UPLOAD STATUS
# ============================================================

def upload_status(
    current,
    total,
    start_time,
):

    elapsed = (
        time.time()
        - start_time
    )

    if elapsed <= 0:
        elapsed = 0.1

    speed = (
        current / elapsed
    )

    if total > 0:

        percentage = (
            current / total
        ) * 100

        remaining = (
            total - current
        )

        eta = (
            remaining / speed
            if speed > 0
            else 0
        )

        bar = progress_bar(
            current,
            total,
        )

        return (
            "📤 **Mode:** `Upload`\n\n"
            f"`{bar}` **{percentage:.1f}%**\n\n"
            f"📦 **File Size:** "
            f"`{format_bytes(current)}` / "
            f"`{format_bytes(total)}`\n"
            f"🚀 **Speed:** "
            f"`{format_bytes(speed)}/s`\n"
            f"⏳ **ETA:** "
            f"`{format_time(eta)}`"
        )

    return (
        "📤 **Mode:** `Upload`\n\n"
        f"📦 **File Size:** "
        f"`{format_bytes(current)}`\n"
        f"🚀 **Speed:** "
        f"`{format_bytes(speed)}/s`\n"
        "⏳ **ETA:** `Calculating...`"
    )


# ============================================================
# VIDEO METADATA
# ============================================================

def get_video_metadata(filepath):

    try:

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-show_entries",
                "stream=width,height,codec_type",
                "-of",
                "json",
                filepath,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return 0, 0, 0

        data = json.loads(
            result.stdout
        )

        duration = 0
        width = 0
        height = 0

        # ----------------------------------------------------
        # Duration
        # ----------------------------------------------------

        duration_value = (
            data
            .get("format", {})
            .get("duration")
        )

        if duration_value:

            try:

                duration = int(
                    float(
                        duration_value
                    )
                )

            except (
                ValueError,
                TypeError,
            ):

                duration = 0

        # ----------------------------------------------------
        # Video dimensions
        # ----------------------------------------------------

        for stream in data.get(
            "streams",
            [],
        ):

            if (
                stream.get(
                    "codec_type"
                )
                == "video"
            ):

                width = int(
                    stream.get(
                        "width"
                    )
                    or 0
                )

                height = int(
                    stream.get(
                        "height"
                    )
                    or 0
                )

                break

        return (
            duration,
            width,
            height,
        )

    except Exception:

        logger.exception(
            "ffprobe error"
        )

        return 0, 0, 0


# ============================================================
# DOWNLOAD FILE
# ============================================================

async def download_file(
    url,
    filepath,
    status_message,
    user_id,
):

    timeout = aiohttp.ClientTimeout(
        total=None,
        connect=30,
        sock_read=120,
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
    }

    downloaded = 0
    total_size = 0

    start_time = time.time()
    last_update = 0

    os.makedirs(
        os.path.dirname(filepath),
        exist_ok=True,
    )

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
                    f"HTTP error: "
                    f"{response.status}"
                )

            content_length = (
                response.headers.get(
                    "Content-Length"
                )
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

            if (
                total_size
                > MAX_FILE_SIZE
            ):

                raise RuntimeError(
                    "File is larger "
                    "than the 4 GB limit."
                )

            with open(
                filepath,
                "wb",
            ) as output:

                async for chunk in (
                    response.content.iter_chunked(
                        CHUNK_SIZE
                    )
                ):

                    # ----------------------------------------
                    # Cancellation
                    # ----------------------------------------

                    if (
                        user_id
                        not in active_downloads
                    ):

                        raise asyncio.CancelledError

                    if not chunk:
                        continue

                    downloaded += len(
                        chunk
                    )

                    # ----------------------------------------
                    # 4 GB limit
                    # ----------------------------------------

                    if (
                        downloaded
                        > MAX_FILE_SIZE
                    ):

                        raise RuntimeError(
                            "File exceeded "
                            "the 4 GB limit."
                        )

                    output.write(
                        chunk
                    )

                    # ----------------------------------------
                    # Progress update
                    # ----------------------------------------

                    now = time.time()

                    if (
                        now - last_update
                        >= PROGRESS_INTERVAL
                    ):

                        try:

                            await status_message.edit_text(
                                download_status(
                                    downloaded,
                                    total_size,
                                    start_time,
                                )
                            )

                        except Exception:
                            pass

                        last_update = now

    return downloaded


# ============================================================
# UPLOAD PROGRESS
# ============================================================

async def upload_progress(
    current,
    total,
    message,
    start_time,
    state,
):

    now = time.time()

    if (
        now - state["last_update"]
        < PROGRESS_INTERVAL
    ):
        return

    state["last_update"] = now

    try:

        await message.edit_text(
            upload_status(
                current,
                total,
                start_time,
            )
        )

    except Exception:
        pass


# ============================================================
# START DOWNLOAD
# ============================================================

async def start_download(
    client,
    message,
    user_id,
    url,
    mode,
):

    # --------------------------------------------------------
    # Already downloading
    # --------------------------------------------------------

    if user_id in active_downloads:

        await message.edit_text(
            "⚠️ **You already have "
            "a download running.**\n\n"
            "Use `/cancel` first."
        )

        return

    # --------------------------------------------------------
    # Validate mode
    # --------------------------------------------------------

    if mode not in (
        "video",
        "document",
    ):

        await message.edit_text(
            "❌ **Invalid download mode.**"
        )

        return

    # --------------------------------------------------------
    # Filename
    # --------------------------------------------------------

    filename = filename_from_url(
        url
    )

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
        "message_id": message.id,
    }

    try:

        # ----------------------------------------------------
        # Preparing
        # ----------------------------------------------------

        await message.edit_text(
            "🔍 **Checking link...**\n\n"
            f"📁 **Mode:** `{mode.title()}`"
        )

        # ----------------------------------------------------
        # Download
        # ----------------------------------------------------

        await download_file(
            url=url,
            filepath=filepath,
            status_message=message,
            user_id=user_id,
        )

        # ----------------------------------------------------
        # Verify file
        # ----------------------------------------------------

        if not os.path.exists(
            filepath
        ):

            raise RuntimeError(
                "Downloaded file not found."
            )

        actual_size = os.path.getsize(
            filepath
        )

        if actual_size <= 0:

            raise RuntimeError(
                "Downloaded file is empty."
            )

        if (
            actual_size
            > MAX_FILE_SIZE
        ):

            raise RuntimeError(
                "File is larger than 4 GB."
            )

        # ----------------------------------------------------
        # Upload start
        # ----------------------------------------------------

        upload_start = time.time()

        upload_state = {
            "last_update": 0,
        }

        await message.edit_text(
            "📤 **Mode:** `Upload`\n\n"
            "📊 **Preparing file...**\n"
            f"📦 **File Size:** "
            f"`{format_bytes(actual_size)}`\n"
            "🚀 **Speed:** `Calculating...`\n"
            "⏳ **ETA:** `Calculating...`"
        )

        # ====================================================
        # VIDEO
        # ====================================================

        if mode == "video":

            (
                duration,
                width,
                height,
            ) = get_video_metadata(
                filepath
            )

            async def progress(
                current,
                total,
            ):

                await upload_progress(
                    current,
                    total,
                    message,
                    upload_start,
                    upload_state,
                )

            sent_message = (
                await client.send_video(
                    chat_id=user_id,
                    video=filepath,
                    caption=DEFAULT_CAPTION,
                    duration=duration,
                    width=width,
                    height=height,
                    supports_streaming=True,
                    progress=progress,
                )
            )

        # ====================================================
        # DOCUMENT
        # ====================================================

        else:

            async def progress(
                current,
                total,
            ):

                await upload_progress(
                    current,
                    total,
                    message,
                    upload_start,
                    upload_state,
                )

            sent_message = (
                await client.send_document(
                    chat_id=user_id,
                    document=filepath,
                    caption=DEFAULT_CAPTION,
                    progress=progress,
                )
            )

        # ----------------------------------------------------
        # Save database history
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
                "Database save failed."
            )

        # ----------------------------------------------------
        # AUTO DELETE
        # ----------------------------------------------------
        #
        # The uploaded Telegram message is scheduled for
        # deletion according to the admin's setting.
        #
        # ----------------------------------------------------

        try:

            from plugins.autodelete import (
                schedule_delete
            )

            asyncio.create_task(
                schedule_delete(
                    client=client,
                    chat_id=user_id,
                    message_id=sent_message.id,
                )
            )

        except Exception:

            logger.exception(
                "Could not schedule auto-delete."
            )

        # ----------------------------------------------------
        # Completed
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "✅ **Completed!**\n\n"
                f"📦 **File Size:** "
                f"`{format_bytes(actual_size)}`\n"
                f"📁 **Mode:** "
                f"`{mode.title()}`"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # Remove status message
        # ----------------------------------------------------

        await asyncio.sleep(2)

        try:

            await message.delete()

        except Exception:
            pass

    except asyncio.CancelledError:

        try:

            await message.edit_text(
                "❌ **Download cancelled.**"
            )

        except Exception:
            pass

    except Exception as error:

        logger.exception(
            "Download failed."
        )

        error_text = str(
            error
        )

        if len(error_text) > 800:

            error_text = (
                error_text[:800]
                + "..."
            )

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

        if os.path.exists(
            filepath
        ):

            try:

                os.remove(
                    filepath
                )

                logger.info(
                    "Deleted temporary file: %s",
                    filepath,
                )

            except Exception:

                logger.exception(
                    "Could not delete "
                    "temporary file."
                )


# ============================================================
# CANCEL DOWNLOAD
# ============================================================

async def cancel_download(
    user_id,
):

    download = active_downloads.pop(
        user_id,
        None,
    )

    if not download:
        return False

    filepath = download.get(
        "filepath"
    )

    if (
        filepath
        and os.path.exists(filepath)
    ):

        try:

            os.remove(
                filepath
            )

            logger.info(
                "Deleted cancelled file: %s",
                filepath,
            )

        except Exception:

            logger.exception(
                "Could not delete "
                "cancelled file."
            )

    return True
