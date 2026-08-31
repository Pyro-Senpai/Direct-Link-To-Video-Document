# config.py

import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# Telegram Configuration
# ============================================================

try:
    API_ID = int(os.getenv("API_ID", "0"))
except ValueError:
    API_ID = 0

API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")


# ============================================================
# MongoDB Configuration
# ============================================================

MONGO_URI = os.getenv("MONGO_URI", "")

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "telegram_link_bot"
)


# ============================================================
# Start Message Image
# ============================================================

START_IMAGE = os.getenv(
    "START_IMAGE",
    "https://telegra.ph/file/8dd38af99889caea1cf4b-2bd9a6e6cfb04c2b95.jpg"
)


# ============================================================
# Download Configuration
# ============================================================

DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    "downloads"
)

# Maximum allowed download size: 4 GB
MAX_FILE_SIZE_GB = 4

MAX_FILE_SIZE = (
    MAX_FILE_SIZE_GB
    * 1024
    * 1024
    * 1024
)


# ============================================================
# Caption
# ============================================================

DEFAULT_CAPTION = os.getenv(
    "DEFAULT_CAPTION",
    "Encoded by @ConverterV22_Bot"
)


# ============================================================
# Create Download Directory
# ============================================================

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# ============================================================
# Validate Configuration
# ============================================================

def validate_config():

    missing = []

    if API_ID == 0:
        missing.append("API_ID")

    if not API_HASH:
        missing.append("API_HASH")

    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")

    if not MONGO_URI:
        missing.append("MONGO_URI")

    if missing:
        raise RuntimeError(
            "Missing environment variables: "
            + ", ".join(missing)
        )


validate_config()
