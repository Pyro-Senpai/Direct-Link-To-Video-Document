Telegram Link Downloader Bot

A Telegram bot built with Python + Pyrogram that allows users to send a direct video/download URL and choose whether the downloaded file should be sent as a Video or Document.

✨ Features

- 🔗 Download files from supported direct URLs
- 🎬 Send downloaded files as Telegram Video
- 📄 Send downloaded files as Telegram Document
- ❌ Cancel active downloads
- 🆔 Short callback IDs instead of putting long URLs inside buttons
- 🔒 User verification for download buttons
- 🌐 Koyeb health-check server
- ⚡ Async downloading with Pyrogram
- 🐍 Python 3.12 compatible
- 🔄 FloodWait handling
- ☁️ Koyeb deployment support

📁 Project Structure

Telegram-Link-Downloader/
│
├── bot.py
├── config.py
├── requirements.txt
├── Dockerfile
├── README.md
│
└── plugins/
    ├── __init__.py
    ├── start.py
    ├── callbacks.py
    ├── cancel.py
    └── downloader.py

🛠️ Requirements

- Python 3.10+
- Telegram Bot Token
- Telegram API ID
- Telegram API Hash
- Pyrogram
- aiohttp

Optional:

- MongoDB, if your downloader/project uses a database
- Koyeb account for cloud deployment

🔑 Get Telegram API ID & API Hash

Go to:

https://my.telegram.org/

1. Log in with your Telegram account.
2. Open API development tools.
3. Create a new application.
4. Copy:
   - "API_ID"
   - "API_HASH"

🤖 Create a Telegram Bot

Open Telegram and search for @BotFather.

Run:

/newbot

Follow the instructions and copy your bot token.

⚙️ Configuration

Create a "config.py" file:

import os

API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

For deployment, it's recommended to use environment variables instead of hard-coding secrets.

📦 Install Dependencies

Clone your project:

git clone YOUR_REPOSITORY_URL
cd Telegram-Link-Downloader

Install dependencies:

pip install -r requirements.txt

Start the bot:

python bot.py

📄 requirements.txt

Example:

Pyrogram>=2.0.106
pyrofork>=2.3.69
pyromod
aiohttp
aiofiles
requests
TgCrypto

Only keep the packages that your actual project imports.

🚀 Deploy on Koyeb

1. Push the project to GitHub

Make sure your repository contains:

bot.py
config.py
requirements.txt
Dockerfile
plugins/

2. Create Koyeb Service

Create a new Web Service from your GitHub repository.

Select your repository and branch.

3. Environment Variables

Add:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

If your project uses additional variables, add them as well.

4. Port

The bot includes an HTTP health server.

Koyeb should use the "PORT" environment variable.

The application defaults to:

8080

Health endpoints:

/

and:

/health

Both return:

OK

5. Start Command

If using a Python build:

python bot.py

If using Docker, configure the Dockerfile to start:

python bot.py

🐳 Dockerfile

Example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]

🎯 How To Use

1. Open your Telegram bot.
2. Send "/start".
3. Send a supported download URL.
4. The bot displays:

🎬 Video
📄 Document
❌ Cancel

5. Select the required format.
6. The bot starts downloading.
7. The completed file is sent back to Telegram.

🔒 Security

The bot creates a short ID for every download request.

Instead of storing the complete URL in Telegram callback data:

video:https://example.com/very/long/url

it uses:

video:a1b2c3d4e5f6

The bot stores the URL internally and verifies that the Telegram user clicking the button is the same user who created the request.

❌ Cancel Download

Users can press:

❌ Cancel

to stop an active download.

If no active download exists, the bot responds:

ℹ️ No active download.

🩺 Koyeb Health Check

The application starts an "aiohttp" web server alongside the Telegram bot.

Example:

Health server started on port 8080

Koyeb can access:

GET /

or:

GET /health

Expected response:

200 OK

🔄 FloodWait Handling

Telegram may temporarily restrict requests when too many API calls are made.

The bot handles "FloodWait" and waits before retrying:

except FloodWait as e:
    wait_time = e.value + 5
    await asyncio.sleep(wait_time)

🐛 Troubleshooting

IndentationError

If you see:

IndentationError: expected an indented block

check the indentation in the affected Python file.

Python requires code inside functions to be indented.

Client is already connected

If you see:

ConnectionError: Client is already connected

make sure your application does not call:

await bot.start()

again after the same Pyrogram client has already connected.

ImportError

Example:

ImportError: cannot import name 'something' from 'config'

Check that the variable exists in "config.py" and that the spelling matches the import.

Bot starts but commands don't work

Check:

- "BOT_TOKEN"
- "API_ID"
- "API_HASH"
- Plugin folder name
- Plugin Python files
- Pyrogram version
- Koyeb logs

📜 License

This project is provided for educational and personal use.

Make sure you have permission to download and redistribute any content processed by the bot.

⭐ Support

If this project helped you, consider giving the repository a ⭐ on GitHub.

---

Made with ❤️ using Python & Pyrogram


If you give me your **actual project file list / `requirements.txt` / `config.py`**, I can make this README match your bot exactly instead of using the generic configuration above.
