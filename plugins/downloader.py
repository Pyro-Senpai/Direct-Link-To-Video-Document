import os
import re
import json
import time
import asyncio
import logging
import subprocess
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
# ACTIVE DOWNLOADS
# ============================================================

active_downloads = {}

# ============================================================
# SETTINGS
# ============================================================

CHUNK_SIZE = 1024 * 1024  # 1 MB
PROGRESS_INTERVAL = 3


# ============================================================
# FORMAT BYTES
# ============================================================

def format_bytes(size: int) -> str:

    if size is None or size <= 0:
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
# FORMAT TIME
# ============================================================

def format_time(seconds: float) -> str:

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

    if hours > 0:
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

def safe_filename(filename: str) -> str:

    filename = unquote(filename)

    filename = os.path.basename(
        filename
    )

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
# FILENAME FROM URL
# ============================================================

def filename_from_url(url: str) -> str:

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
    current: int,
    total: int,
    length: int = 12,
) -> str:

    if total <= 0:
        return "○" * length

    percentage = current / total

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
        + "○" * (length - filled)
    )


# ============================================================
# DOWNLOAD PROGRESS TEXT
# ============================================================

def make_download_progress(
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

        bar = progress_bar(
            current,
            total,
            12,
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
# UPLOAD PROGRESS TEXT
# ============================================================

def make_upload_progress(
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

        bar = progress_bar(
            current,
            total,
            12,
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
# UPDATE DOWNLOAD PROGRESS
# ============================================================

async def update_download_progress(
    message: Message,
    current: int,
    total: int,
    start_time: float,
):

    try:

        text = make_download_progress(
            current,
            total,
            start_time,
        )

        await message.edit_text(
            text
        )

    except Exception:
        pass


# ============================================================
# UPLOAD PROGRESS CALLBACK
# ============================================================

async def upload_progress_callback(
    current: int,
    total: int,
    message: Message,
    start_time: float,
    state: dict,
):

    now = time.time()

    # Avoid editing Telegram message too frequently.
    if (
        now - state.get(
            "last_update",
            0,
        )
        < PROGRESS_INTERVAL
    ):
        return

    state["last_update"] = now

    try:

        text = make_upload_progress(
            current,
            total,
            start_time,
        )

        await message.edit_text(
            text
        )

    except Exception:
        pass


# ============================================================
# VIDEO METADATA
# ============================================================

def get_video_metadata(filepath: str):

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

            logger.warning(
                "ffprobe failed: %s",
                result.stderr[:500],
            )

            return 0, 0, 0

        data = json.loads(
            result.stdout
        )

        duration = 0
        width = 0
        height = 0

        # ----------------------------------------------------
        # DURATION
        # ----------------------------------------------------

        format_data = data.get(
            "format",
            {},
        )

        duration_value = format_data.get(
            "duration"
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
        # WIDTH / HEIGHT
        # ----------------------------------------------------

        for stream in data.get(
            "streams",
            [],
        ):

            if stream.get(
                "codec_type"
            ) == "video":

                try:

                    width = int(
                        stream.get(
                            "width"
                        ) or 0
                    )

                except Exception:

                    width = 0

                try:

                    height = int(
                        stream.get(
                            "height"
                        ) or 0
                    )

                except Exception:

                    height = 0

                break

        logger.info(
            "Video metadata: "
            "duration=%s width=%s height=%s",
            duration,
            width,
            height,
        )

        return (
            duration,
            width,
            height,
        )

    except FileNotFoundError:

        logger.error(
            "ffprobe is not installed."
        )

        return 0, 0, 0

    except Exception:

        logger.exception(
            "Failed to read video metadata."
        )

        return 0, 0, 0


# ============================================================
# DOWNLOAD FILE
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
                    f"HTTP error: {response.status}"
                )

            # ------------------------------------------------
            # CONTENT LENGTH
            # ------------------------------------------------

            content_length = response.headers.get(
                "Content-Length"
            )

            if content_length:

                try:

                    total_size = int(
                        content_length
                    )

                except (
                    ValueError,
                    TypeError,
                ):

                    total_size = 0

            # ------------------------------------------------
            # CHECK 4 GB LIMIT
            # ------------------------------------------------

            if total_size > MAX_FILE_SIZE:

                raise RuntimeError(
                    "The file is larger than "
                    "the 4 GB limit."
                )

            # ------------------------------------------------
            # STREAM TO DISK
            # ------------------------------------------------

            with open(
                filepath,
                "wb",
            ) as output:

                async for chunk in response.content.iter_chunked(
                    CHUNK_SIZE
                ):

                    # ----------------------------------------
                    # CANCEL CHECK
                    # ----------------------------------------

                    if user_id not in active_downloads:

                        raise asyncio.CancelledError

                    if not chunk:
                        continue

                    downloaded += len(chunk)

                    # ----------------------------------------
                    # 4 GB CHECK
                    # ----------------------------------------

                    if downloaded > MAX_FILE_SIZE:

                        raise RuntimeError(
                            "The file exceeded "
                            "the 4 GB limit."
                        )

                    output.write(
                        chunk
                    )

                    # ----------------------------------------
                    # PROGRESS
                    # ----------------------------------------

                    now = time.time()

                    if (
                        now - last_update
                        >= PROGRESS_INTERVAL
                    ):

                        await update_download_progress(
                            status_message,
                            downloaded,
                            total_size,
                            start_time,
                        )

                        last_update = now

    return downloaded


# ============================================================
# START DOWNLOAD
# ============================================================

async def start_download(
    client: Client,
    message: Message,
    user_id: int,
    url: str,
    mode: str,
):

    # --------------------------------------------------------
    # ALREADY DOWNLOADING
    # --------------------------------------------------------

    if user_id in active_downloads:

        try:

            await message.edit_text(
                "⚠️ **You already have a download running.**\n\n"
                "Use `/cancel` to stop it."
            )

        except Exception:
            pass

        return

    # --------------------------------------------------------
    # VALIDATE MODE
    # --------------------------------------------------------

    if mode not in (
        "video",
        "document",
    ):

        try:

            await message.edit_text(
                "❌ **Invalid mode.**"
            )

        except Exception:
            pass

        return

    # --------------------------------------------------------
    # FILENAME
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
    # REGISTER DOWNLOAD
    # --------------------------------------------------------

    active_downloads[user_id] = {
        "url": url,
        "filepath": filepath,
        "mode": mode,
        "started_at": time.time(),
    }

    try:

        # ----------------------------------------------------
        # CHECKING
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "🔍 **Checking download link...**"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        await download_file(
            url=url,
            filepath=filepath,
            status_message=message,
            user_id=user_id,
        )

        # ----------------------------------------------------
        # FILE CHECK
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
        # UPLOAD STATE
        # ----------------------------------------------------

        upload_start = time.time()

        upload_state = {
            "last_update": 0,
        }

        # ----------------------------------------------------
        # UPLOAD STATUS
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "📤 **Mode:** `Upload`\n\n"
                "📊 **Preparing file...**\n"
                f"📦 **File Size:** "
                f"`{format_bytes(actual_size)}`\n"
                "🚀 **Speed:** `Calculating...`\n"
                "⏳ **ETA:** `Calculating...`"
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # CAPTION
        # ----------------------------------------------------

        caption = DEFAULT_CAPTION

        # ----------------------------------------------------
        # VIDEO
        # ----------------------------------------------------

        if mode == "video":

            (
                duration,
                width,
                height,
            ) = get_video_metadata(
                filepath
            )

            logger.info(
                "Uploading video: "
                "duration=%s width=%s height=%s",
                duration,
                width,
                height,
            )

            async def video_progress(
                current,
                total,
            ):

                await upload_progress_callback(
                    current,
                    total,
                    message,
                    upload_start,
                    upload_state,
                )

            await client.send_video(
                chat_id=user_id,
                video=filepath,
                caption=caption,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                progress=video_progress,
            )

        # ----------------------------------------------------
        # DOCUMENT
        # ----------------------------------------------------

        elif mode == "document":

            async def document_progress(
                current,
                total,
            ):

                await upload_progress_callback(
                    current,
                    total,
                    message,
                    upload_start,
                    upload_state,
                )

            await client.send_document(
                chat_id=user_id,
                document=filepath,
                caption=caption,
                progress=document_progress,
            )

        # ----------------------------------------------------
        # DATABASE
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
        # COMPLETED
        # ----------------------------------------------------

        try:

            await message.edit_text(
                "✅ **Completed Successfully!**\n\n"
                f"📦 **File Size:** "
                f"`{format_bytes(actual_size)}`\n"
                f"📁 **Mode:** `{mode.title()}`"
            )

        except Exception:
            pass

        await asyncio.sleep(2)

        try:
            await message.delete()
        except Exception:
            pass

    except asyncio.CancelledError:

        logger.info(
            "Download cancelled: %s",
            user_id,
        )

        try:

            await message.edit_text(
                "❌ **Download cancelled.**"
            )

        except Exception:
            pass

    except aiohttp.ClientError as error:

        logger.error(
            "HTTP download error: %s",
            error,
        )

        try:

            await message.edit_text(
                "❌ **Download failed.**\n\n"
                "Unable to connect to the server."
            )

        except Exception:
            pass

    except Exception as error:

        logger.exception(
            "Download failed for user %s",
            user_id,
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
        # REMOVE ACTIVE DOWNLOAD
        # ----------------------------------------------------

        active_downloads.pop(
            user_id,
            None,
        )

        # ----------------------------------------------------
        # DELETE TEMP FILE
        #
        # IMPORTANT FOR KOYEB:
        # Don't keep large files on the 500 MB disk.
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
# CANCEL DOWNLOAD
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
    # download_file() to stop on the next chunk.

    active_downloads.pop(
        user_id,
        None,
    )

    filepath = download.get(
        "filepath"
    )

    if filepath and os.path.exists(filepath):

        try:

            os.remove(filepath)

            logger.info(
                "Deleted cancelled file: %s",
                filepath,
            )

        except Exception:

            logger.exception(
                "Failed to delete cancelled file."
            )

    return True
