# Telegram Link Downloader Bot

A simple and powerful Telegram bot that downloads files from supported direct links and sends them back to users through Telegram.

Built with Python, Pyrogram and Aiohttp, with support for Koyeb deployment.

Features

- 🔗 Download files from direct URLs
- 🎬 Send downloads as Video
- 📄 Send downloads as Document
- ❌ Cancel active downloads
- 🔒 User-specific download requests
- 🆔 Temporary callback IDs
- ⚡ Asynchronous processing
- 🌐 Koyeb health-check server
- 🐳 Docker support
- 🔄 FloodWait handling
- 🧩 Modular plugin structure

How It Works

User sends URL
      ↓
Bot receives URL
      ↓
Choose Video / Document
      ↓
Download starts
      ↓
File is sent to Telegram

Project Structure

.
├── bot.py
├── config.py
├── requirements.txt
├── Dockerfile
├── README.md
│
└── plugins/
    ├── start.py
    ├── callbacks.py
    ├── downloader.py
    └── cancel.py

Requirements

- Python 3.10+
- Telegram Bot Token
- Telegram API ID
- Telegram API Hash

Main Python packages:

Pyrogram
Pyrofork
Pyromod
Aiohttp
Aiofiles
TgCrypto

Configuration

Set the following environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

Do not publish your "BOT_TOKEN" or "API_HASH".

Local Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL
cd LINK-DOWNLOADER

Install dependencies:

pip install -r requirements.txt

Start the bot:

python bot.py

Koyeb Deployment

This bot includes an Aiohttp health server for cloud platforms such as Koyeb.

Set these environment variables in Koyeb:

API_ID
API_HASH
BOT_TOKEN

Start command:

python bot.py

The health server uses the "PORT" environment variable and falls back to port "8080".

Health endpoints:

/
 /health

Both endpoints return:

OK

Docker

Build the image:

docker build -t telegram-link-downloader .

Run:

docker run telegram-link-downloader

Callback Security

The bot does not place the complete URL inside Telegram callback data.

Instead, it generates a temporary ID:

video:a91f42c8d301

The bot stores the relationship between:

Short ID
   ↓
User ID
   ↓
Download URL

Before starting a download, the bot checks that the button belongs to the user who created the request.

Error Handling

The bot handles Telegram "FloodWait" errors by waiting before retrying.

Unexpected startup errors are logged so they can be diagnosed from the deployment logs.

If the same Pyrogram client is started multiple times, you may see:

ConnectionError: Client is already connected

Make sure "bot.start()" is not being called repeatedly on an already-connected client.

Troubleshooting

IndentationError

Check the indentation of functions, loops and conditional blocks.

Example:

async def example():
    print("Hello")

ImportError

Make sure the imported function exists in the referenced plugin.

Example:

from plugins.downloader import start_download

Verify:

plugins/downloader.py

contains "start_download".

Koyeb Health Check Failed

Check:

1. The application listens on "0.0.0.0".
2. The "PORT" environment variable is used.
3. "/" returns HTTP 200.
4. All required environment variables are configured.
5. "requirements.txt" installs successfully.
6. There are no Python syntax or import errors.

Security

Never commit sensitive credentials to GitHub.

Use environment variables for:

API_ID
API_HASH
BOT_TOKEN

If a bot token is accidentally exposed, regenerate it immediately through BotFather.

Future Plans

- Download progress
- Download queue
- Download history
- Admin controls
- User settings
- Statistics
- Database support
- Improved error messages

Disclaimer

This project is intended for educational and legitimate use.

Only download content that you have permission to access and download. Respect copyright laws and the terms of service of the websites and services you use.

License

This project is provided for educational and personal use.

---

Made with ❤️ using Python & Pyrogram

⭐ If you find this project useful, consider giving the repository a star.
