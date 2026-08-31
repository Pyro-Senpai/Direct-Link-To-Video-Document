import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# Telegram
# ============================================================

try:
    API_ID = int(os.getenv("API_ID", "0"))
except ValueError:
    API_ID = 0

API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")


# ============================================================
# MongoDB
# ============================================================

MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "telegram_link_bot"
)


# ============================================================
# Download
# ============================================================

DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    "downloads"
)

try:
    MAX_FILE_SIZE_MB = int(
        os.getenv("MAX_FILE_SIZE_MB", "2000")
    )
except ValueError:
    MAX_FILE_SIZE_MB = 2000

MAX_FILE_SIZE = (
    MAX_FILE_SIZE_MB * 1024 * 1024
)


# ============================================================
# Caption
# ============================================================

DEFAULT_CAPTION = os.getenv(
    "DEFAULT_CAPTION",
    "Downloaded by @YourBot"
)


# ============================================================
# Create Download Directory
# ============================================================

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)


# ============================================================
# Configuration Validation
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
