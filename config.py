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
# Admin Configuration
# ============================================================

try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
except ValueError:
    ADMIN_ID = 0


# ============================================================
# MongoDB Configuration
# ============================================================

MONGO_URI = os.getenv("MONGO_URI", "")

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

# Maximum download size: 4 GB
MAX_FILE_SIZE_GB = 4

MAX_FILE_SIZE = (
    MAX_FILE_SIZE_GB
    * 1024
    * 1024
    * 1024
)


# ============================================================
# Auto Delete Configuration
# ============================================================

# Default: 0 = disabled
DEFAULT_AUTO_DELETE = int(
    os.getenv("DEFAULT_AUTO_DELETE", "0")
)

# Minimum auto-delete time: 5 seconds
MIN_AUTO_DELETE = 5

# Maximum auto-delete time: 7 days
MAX_AUTO_DELETE = (
    7 * 24 * 60 * 60
)


# ============================================================
# Caption
# ============================================================

DEFAULT_CAPTION = os.getenv(
    "DEFAULT_CAPTION",
    "Downloaded by @YourBot"
)

# ============================================================
# Start Image
# ============================================================

START_IMAGE = os.getenv(
"START_IMAGE",
"https://telegra.ph/file/aad055c98c566adfb7dcd-b42f72ff4d1de29e86.jpg"
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

    if ADMIN_ID == 0:
        missing.append("ADMIN_ID")

    if missing:
        raise RuntimeError(
            "Missing environment variables: "
            + ", ".join(missing)
        )


validate_config()
