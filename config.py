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
    "<b><blockquote>📚 ʜᴇʟᴘ & ɢᴜɪᴅᴇ\n"
    "🔗 ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ\n"
    "1. ꜱᴇɴᴅ ᴀ ᴅɪʀᴇᴄᴛ ʜᴛᴛᴘ/ʜᴛᴛᴘꜱ ꜰɪʟᴇ ʟɪɴᴋ.\n"
    "2. ᴄʜᴏᴏꜱᴇ 🎬 ᴠɪᴅᴇᴏ ᴏʀ 📄 ᴅᴏᴄᴜᴍᴇɴᴛ.\n"
    "3. ᴡᴀɪᴛ ᴡʜɪʟᴇ ᴛʜᴇ ꜰɪʟᴇ ɪꜱ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ.\n"
    "4. ᴛʜᴇ ʙᴏᴛ ᴜᴘʟᴏᴀᴅꜱ ᴛʜᴇ ꜰɪʟᴇ ᴛᴏ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ.</blockquote>\n"
    "<blockquote>🎬 ᴠɪᴅᴇᴏ\n"
    "ᴛʜᴇ ꜰɪʟᴇ ɪꜱ ᴜᴘʟᴏᴀᴅᴇᴅ ᴀꜱ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴠɪᴅᴇᴏ.\n"
    "📄 ᴅᴏᴄᴜᴍᴇɴᴛ\n"
    "ᴛʜᴇ ꜰɪʟᴇ ɪꜱ ᴜᴘʟᴏᴀᴅᴇᴅ ᴀꜱ ᴀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴏᴄᴜᴍᴇɴᴛ.\n"
    "🔄 ʀᴇꜰʀᴇꜱʜ\n"
    "ʀᴇꜰʀᴇꜱʜᴇꜱ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ/ᴜᴘʟᴏᴀᴅ ᴘʀᴏɢʀᴇꜱꜱ.\n"
    "❌ ᴄᴀɴᴄᴇʟ\n"
    "ꜱᴛᴏᴘꜱ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴅᴏᴡɴʟᴏᴀᴅ ᴏʀ ᴜᴘʟᴏᴀᴅ ᴘʀᴏᴄᴇꜱꜱ.\n"
    "🗑️ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ\n"
    "ᴜᴘʟᴏᴀᴅᴇᴅ ꜰɪʟᴇꜱ ᴄᴀɴ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴀꜰᴛᴇʀ "
    "ᴛʜᴇ ᴄᴏɴꜰɪɢᴜʀᴇᴅ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ.</blockquote></b>"
)

ABOUT_TEXT = (
    "<b>ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ\n"
    "<blockquote>ᴛᴇʟᴇɢʀᴀᴍ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ\n"
    "ᴀ ꜰᴀꜱᴛ ᴀɴᴅ ꜱɪᴍᴘʟᴇ ᴅɪʀᴇᴄᴛ-ʟɪɴᴋ ꜰɪʟᴇ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ "
    "ʙᴜɪʟᴛ ꜰᴏʀ ᴛᴇʟᴇɢʀᴀᴍ.</blockquote>\n"
    "<blockquote>ꜰᴇᴀᴛᴜʀᴇꜱ\n"
    "• ᴅɪʀᴇᴄᴛ ʜᴛᴛᴘ/ʜᴛᴛᴘꜱ ᴅᴏᴡɴʟᴏᴀᴅꜱ\n"
    "• ᴠɪᴅᴇᴏ & ᴅᴏᴄᴜᴍᴇɴᴛ ꜱᴜᴘᴘᴏʀᴛ\n"
    "• ʟɪᴠᴇ ᴅᴏᴡɴʟᴏᴀᴅ ᴘʀᴏɢʀᴇꜱꜱ\n"
    "• ʟɪᴠᴇ ᴜᴘʟᴏᴀᴅ ᴘʀᴏɢʀᴇꜱꜱ\n"
    "• ʀᴇꜰʀᴇꜱʜ & ᴄᴀɴᴄᴇʟ ᴄᴏɴᴛʀᴏʟꜱ\n"
    "• ᴀᴜᴛᴏᴍᴀᴛɪᴄ ꜰɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ\n"
    "• ᴍᴏɴɢᴏᴅʙ ᴅᴀᴛᴀʙᴀꜱᴇ ꜱᴜᴘᴘᴏʀᴛ\n"
    "• ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ꜱᴜᴘᴘᴏʀᴛ</blockquote></b>"
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
