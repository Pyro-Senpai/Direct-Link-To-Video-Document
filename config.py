# config.py

import os
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

logger = logging.getLogger(__name__)


# ============================================================
# Telegram Configuration
# ============================================================

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")


# ============================================================
# MongoDB Configuration
# ============================================================

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "telegram_link_bot"
)


# ============================================================
# Download Configuration
# ============================================================

DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    "downloads"
)

# Maximum download size in MB
MAX_FILE_SIZE_MB = int(
    os.getenv(
        "MAX_FILE_SIZE_MB",
        "2000"
    )
)

MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024


# ============================================================
# Telegram Upload Configuration
# ============================================================

# Caption shown with downloaded files
DEFAULT_CAPTION = os.getenv(
    "DEFAULT_CAPTION",
    "Downloaded by @YourBot"
)


# ============================================================
# Validation
# ============================================================

def validate_config():

    required = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "MONGO_URI": MONGO_URI,
    }

    missing = [
        name
        for name, value in required.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )

    try:
        global API_ID
        API_ID = int(API_ID)

    except (ValueError, TypeError):
        raise RuntimeError(
            "API_ID must be a valid integer."
        )


# ============================================================
# Create Download Directory
# ============================================================

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# ============================================================
# Validate on Import
# ============================================================

validate_config()
