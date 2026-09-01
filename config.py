import os
from dotenv import load_dotenv

load_dotenv()

try:
    API_ID = int(os.getenv("API_ID", "0"))
except ValueError:
    API_ID = 0

API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
except ValueError:
    ADMIN_ID = 0

MONGO_URI = os.getenv("MONGO_URI", "")

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "telegram_link_bot"
)

DOWNLOAD_DIR = os.getenv(
    "DOWNLOAD_DIR",
    "downloads"
)

MAX_FILE_SIZE_GB = 4

MAX_FILE_SIZE = (
    MAX_FILE_SIZE_GB
    * 1024
    * 1024
    * 1024
)

DEFAULT_AUTO_DELETE = int(
    os.getenv("DEFAULT_AUTO_DELETE", "0")
)

MIN_AUTO_DELETE = 5

MAX_AUTO_DELETE = (
    7 * 24 * 60 * 60
)

DEFAULT_CAPTION = os.getenv(
    "DEFAULT_CAPTION",
    "Encoded by @ConverterV22_Bot"
)

START_IMAGE = os.getenv(
    "START_IMAGE",
    "https://telegra.ph/file/aad055c98c566adfb7dcd-b42f72ff4d1de29e86.jpg"
)

START_TEXT = (
    """<b>💖 ʜᴇʟʟᴏ {mention} 🥀,\n<blockquote>ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ᴅɪʀᴇᴄᴛ ʟɪɴᴋ ᴛᴏ ᴠɪᴅᴇᴏ / ᴅᴏᴄᴜᴍᴇɴᴛ ᴄᴏɴᴄᴇʀᴛᴇʀ ʙᴏᴛ</blockquote>\n<blockquote>ᴛʜɪs ɪs ᴍʏ sᴇɴᴘᴀɪ - <a href=" https://t.me/PyroSznpai">ᴘʏʀᴏ sᴇɴᴘᴀɪ</a></blockquote></b>"""
)

HELP_TEXT = (
    "<b><blockquote>📚 **Help & Guide**\n"
    "🔗 **How to Download**\n"
    "1. Send a direct HTTP/HTTPS file link.\n"
    "2. Choose **🎬 Video** or **📄 Document**.\n"
    "3. Wait while the file is downloading.\n"
    "4. The bot uploads the file to your Telegram.</blockquote>\n"
    "<blockquote>🎬 **Video**\n"
    "The file is uploaded as a Telegram video.\n"
    "📄 **Document**\n"
    "The file is uploaded as a Telegram document.\n"
    "🔄 **Refresh**\n"
    "Refreshes the current download/upload progress.\n"
    "❌ **Cancel**\n"
    "Stops the current download or upload process.\n"
    "🗑️ **Auto Delete**\n"
    "Uploaded files can be automatically deleted after "
    "the configured auto-delete time.</blockquote></b>"
)

ABOUT_TEXT = (
    "<b>**About This Bot**\n"
    "<blockquote>**Telegram File Store Bot**\n"
    "A fast and simple direct-link file downloader "
    "built for Telegram.</blockquote>\n"
    "<blockquote>**Features**\n"
    "• Direct HTTP/HTTPS downloads\n"
    "• Video & Document support\n"
    "• Live download progress\n"
    "• Live upload progress\n"
    "• Refresh & Cancel controls\n"
    "• Automatic file deletion\n"
    "• MongoDB database support\n"
    "• Force subscription support</blockquote></b>"
)

os.makedirs(
    DOWNLOAD_DIR,
    exist_ok=True
)

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
