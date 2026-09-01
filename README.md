🚀 Telegram Link Downloader Bot

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Pyrogram-2.x-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Koyeb-Deploy-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram" />
</p><p align="center">
  <b>⚡ A powerful Telegram Link Downloader Bot built with Python & Pyrogram.</b>
</p>---

✨ Features

<table>
<tr>
<td>🔗 <b>URL Download</b></td>
<td>🎬 <b>Video Mode</b></td>
</tr>
<tr>
<td>📄 <b>Document Mode</b></td>
<td>❌ <b>Cancel Download</b></td>
</tr>
<tr>
<td>🔒 <b>User Security</b></td>
<td>🆔 <b>Short Callback IDs</b></td>
</tr>
<tr>
<td>☁️ <b>Koyeb Support</b></td>
<td>⚡ <b>Async Processing</b></td>
</tr>
</table>---

🧰 Tech Stack

🐍 Python
⚡ Pyrogram
🌐 Aiohttp
☁️ Koyeb
📦 Aiofiles

---

📁 Project Structure

Telegram-Link-Downloader/
│
├── 📄 bot.py
├── 📄 config.py
├── 📄 requirements.txt
├── 📄 Dockerfile
├── 📄 README.md
│
└── 📂 plugins/
    ├── 📄 __init__.py
    ├── 📄 start.py
    ├── 📄 callbacks.py
    ├── 📄 cancel.py
    └── 📄 downloader.py

---

🔑 Environment Variables

Create the following environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

«⚠️ Never publish your "BOT_TOKEN" or "API_HASH" publicly.»

---

🤖 Create Your Telegram Bot

Open Telegram and search for:

@BotFather

Then use:

/newbot

Follow the instructions and copy your bot token.

---

🔐 Get API ID & API HASH

Open:

https://my.telegram.org/

Then:

Login
  ↓
API Development Tools
  ↓
Create New Application
  ↓
Copy API_ID & API_HASH

---

📦 Installation

1️⃣ Clone Repository

git clone YOUR_REPOSITORY_URL
cd Telegram-Link-Downloader

2️⃣ Install Requirements

pip install -r requirements.txt

3️⃣ Start Bot

python bot.py

---

📋 requirements.txt

Pyrogram>=2.0.106
pyrofork>=2.3.69
pyromod
aiohttp
aiofiles
requests
TgCrypto

---

🎯 How It Works

👤 User
   │
   │ Sends URL
   ▼
🤖 Telegram Bot
   │
   ▼
🎬 Video     📄 Document
   │              │
   └──────┬───────┘
          ▼
     📥 Download
          │
          ▼
     📤 Send File
          │
          ▼
       👤 User

---

🎬 Download Format

When a user sends a URL, the bot shows:

┌─────────────────────────────────┐
│     📥 Choose download format   │
├─────────────────────────────────┤
│  🎬 Video     │  📄 Document   │
├─────────────────────────────────┤
│          ❌ Cancel              │
└─────────────────────────────────┘

🎬 Video

The downloaded file is sent as a Telegram video.

📄 Document

The downloaded file is sent as a Telegram document.

❌ Cancel

Cancels the user's active download.

---

🔒 Security

The bot doesn't put the full URL inside Telegram's callback data.

Instead:

Full URL
   ↓
Generate Short ID
   ↓
Store URL
   ↓
Send Button

Example:

video:a1b2c3d4e5f6

The bot also verifies the Telegram user ID before starting the download.

---

☁️ Koyeb Deployment

Step 1 — Upload to GitHub

Push your project to GitHub.

Step 2 — Create Koyeb App

Create a new Web Service and connect your GitHub repository.

Step 3 — Add Environment Variables

API_ID
API_HASH
BOT_TOKEN

Step 4 — Port

The health server uses:

8080

or Koyeb's:

PORT

environment variable.

Step 5 — Start Command

python bot.py

---

🩺 Health Check

The bot includes an "aiohttp" health server.

GET /

Response:

OK

Another endpoint:

GET /health

Response:

OK

This allows Koyeb to verify that the service is running.

---

🐳 Docker

Example "Dockerfile":

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]

---

🐛 Troubleshooting

❌ IndentationError

Check the indentation of your Python files.

Example:

async def test():
    print("Hello")

Not:

async def test():
print("Hello")

---

❌ Client is already connected

Make sure the same Pyrogram client isn't being started multiple times.

Use:

await bot.start()

only once for the application lifecycle.

---

❌ ImportError

Check that the imported function or variable actually exists.

Example:

from plugins.downloader import start_download

Make sure "start_download" exists inside:

plugins/downloader.py

---

⚠️ Important

This bot should only be used to download content that you have permission to access or download.

Do not use it to bypass access controls, copyright restrictions, or website security mechanisms.

---

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork the repository
🐛 Report bugs
💡 Suggest improvements

---

📜 License

This project is provided for educational and personal use.

---

<p align="center"><b>🚀 Telegram Link Downloader Bot</b>

<br>Made with ❤️ using Python & Pyrogram

</p>
