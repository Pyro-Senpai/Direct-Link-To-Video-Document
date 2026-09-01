<div align="center">⚡ LINK-DROP

"Advanced Telegram Link Downloader"

URL → Download → Telegram

<br>"Python" (https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
"Pyrogram" (https://img.shields.io/badge/Pyrogram-2.x-2CA5E0?style=for-the-badge)
"Async" (https://img.shields.io/badge/Architecture-Async-00B894?style=for-the-badge)
"Koyeb" (https://img.shields.io/badge/Deploy-Koyeb-6C5CE7?style=for-the-badge)

<br>⚡ Fast • 🧩 Modular • 🔒 Secure • ☁️ Cloud Ready

</div>---

<div align="center">╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                  ⚡ LINK-DROP ENGINE                     ║
║                                                          ║
║          DIRECT URL  ───────►  TELEGRAM FILE             ║
║                                                          ║
║        Built with Python + Pyrogram + Aiohttp             ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

</div>🧠 01 — Overview

LINK-DROP is an asynchronous Telegram download bot designed around a modular plugin architecture.

The bot accepts a supported downloadable URL, creates a protected temporary request, allows the user to select the output format, downloads the content and sends the result back through Telegram.

┌─────────────┐
│ 👤 USER     │
└──────┬──────┘
       │
       │ 🔗 URL
       ▼
┌─────────────────────┐
│ 🤖 LINK-DROP        │
│ Request Manager     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 🆔 Temporary ID     │
│ User + URL Mapping  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────────┐
│     📥 FORMAT SELECTOR      │
├──────────────┬──────────────┤
│  🎬 VIDEO    │ 📄 DOCUMENT  │
└──────────────┴──────────────┘
          │
          ▼
┌─────────────────────┐
│ 📥 DOWNLOAD ENGINE  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ 📤 TELEGRAM OUTPUT │
└─────────────────────┘

---

🚀 02 — Feature Matrix

Feature| Status
🔗 Direct URL handling| ✅
🎬 Video output| ✅
📄 Document output| ✅
❌ Download cancellation| ✅
🆔 Temporary request IDs| ✅
🔒 User ownership validation| ✅
⚡ Async processing| ✅
🧩 Plugin architecture| ✅
🌐 HTTP health server| ✅
☁️ Koyeb deployment| ✅
🔄 FloodWait handling| ✅
🐳 Docker support| ✅

---

🏗️ 03 — Architecture

                         ┌──────────────────┐
                         │    TELEGRAM      │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │       PYROGRAM          │
                    │      BOT CLIENT         │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 │               │               │
                 ▼               ▼               ▼
          ┌────────────┐  ┌────────────┐  ┌────────────┐
          │   START    │  │ CALLBACKS  │  │   CANCEL   │
          │   PLUGIN   │  │   PLUGIN   │  │   PLUGIN   │
          └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                │               │               │
                └───────────────┼───────────────┘
                                ▼
                       ┌────────────────┐
                       │    DOWNLOADER  │
                       │     ENGINE     │
                       └───────┬────────┘
                               │
                               ▼
                         📦 FILE OUTPUT

---

📂 04 — Project Structure

LINK-DROP/
│
├── 🤖 bot.py
│
├── ⚙️ config.py
│
├── 📦 requirements.txt
│
├── 🐳 Dockerfile
│
├── 📖 README.md
│
└── 🧩 plugins/
    │
    ├── 🚀 start.py
    │
    ├── 🎛️ callbacks.py
    │
    ├── 📥 downloader.py
    │
    └── ❌ cancel.py

Responsibility Map

bot.py
   └── Application lifecycle + health server

start.py
   └── /start + URL processing

callbacks.py
   └── Video / Document / Cancel buttons

downloader.py
   └── Download execution

cancel.py
   └── Download cancellation

config.py
   └── Environment configuration

---

🔐 05 — Request Security

LINK-DROP avoids putting the complete URL into Telegram's "callback_data".

Instead:

                    ORIGINAL URL
                         │
                         ▼
                ┌─────────────────┐
                │ Generate UUID    │
                └────────┬────────┘
                         │
                         ▼
                   SHORT ID
                         │
                         ▼
             ┌─────────────────────┐
             │ User ID + URL       │
             │ stored temporarily  │
             └─────────┬───────────┘
                       │
                       ▼
                  TELEGRAM BUTTON

Example:

video:a91f42c8d301

The callback handler verifies:

Clicked User ID
       │
       ▼
Stored User ID
       │
       ├── MATCH ──► Continue
       │
       └── NO MATCH ──► Reject

Response for an unauthorized user:

╔══════════════════════════════════╗
║ 🔒 ACCESS DENIED                 ║
║                                  ║
║ ❌ This button belongs to        ║
║    another user.                 ║
╚══════════════════════════════════╝

---

🎛️ 06 — Interactive UI

When a URL is received:

╔════════════════════════════════════════╗
║        📥 CHOOSE DOWNLOAD FORMAT       ║
╠══════════════════╦═════════════════════╣
║    🎬 VIDEO      ║    📄 DOCUMENT      ║
╠══════════════════╩═════════════════════╣
║              ❌ CANCEL                  ║
╚════════════════════════════════════════╝

🎬 Video

Sends the result as a Telegram video.

📄 Document

Sends the result as a Telegram document.

❌ Cancel

Attempts to stop the active download for that user.

---

⚙️ 07 — Configuration

Environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

Optional project-specific variables can be added through your deployment environment.

🔒 Secret Policy

╔════════════════════════════════════════╗
║              🔐 SECRETS                ║
╠════════════════════════════════════════╣
║ ❌ Don't commit BOT_TOKEN              ║
║ ❌ Don't commit API_HASH               ║
║ ❌ Don't publish private credentials   ║
║                                        ║
║ ✅ Use environment variables           ║
╚════════════════════════════════════════╝

---

🧪 08 — Local Development

Clone:

git clone YOUR_REPOSITORY_URL
cd LINK-DROP

Install:

pip install -r requirements.txt

Run:

python bot.py

Expected startup:

╔════════════════════════════════════════╗
║          🚀 LINK-DROP STARTUP         ║
╠════════════════════════════════════════╣
║ 🌐 Health server      : ONLINE        ║
║ 🔌 Telegram client    : CONNECTING    ║
║ 🤖 Bot                : STARTING      ║
╚════════════════════════════════════════╝

---

☁️ 09 — Koyeb Deployment

                 ┌──────────────┐
                 │    GitHub    │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │    KOYEB     │
                 ├──────────────┤
                 │ Build        │
                 │ Deploy       │
                 │ Health Check │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │  LINK-DROP   │
                 │   ONLINE     │
                 └──────────────┘

Environment

API_ID
API_HASH
BOT_TOKEN

Start Command

python bot.py

---

🩺 10 — Health System

LINK-DROP runs an "aiohttp" HTTP server alongside the Telegram client.

┌──────────────────────────────┐
│        KOYEB CHECK            │
├──────────────────────────────┤
│                              │
│ GET /                        │
│ GET /health                  │
│                              │
│ Response:                    │
│ HTTP 200 → OK                │
│                              │
└──────────────────────────────┘

Port selection:

PORT environment variable
          │
          ▼
       Available?
       /        \
     YES         NO
      │           │
      ▼           ▼
   Use PORT     8080

---

🔄 11 — Error Recovery

The application treats Telegram "FloodWait" differently from unexpected startup failures.

                 ERROR
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      FloodWait        Other Error
          │                 │
          ▼                 ▼
      Wait + Retry      Log + Exit
                            │
                            ▼
                     Cloud Restart

This avoids repeatedly calling "bot.start()" on an already-connected Pyrogram client.

---

📦 12 — Dependencies

Typical runtime dependencies:

┌───────────────────────────────────┐
│ Python 3.12                      │
├───────────────────────────────────┤
│ Pyrogram                         │
│ Pyrofork                         │
│ Pyromod                          │
│ Aiohttp                          │
│ Aiofiles                         │
│ TgCrypto                         │
└───────────────────────────────────┘

Always use the exact versions specified in your project's "requirements.txt".

---

🐳 13 — Docker

Example:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]

Build:

docker build -t link-drop .

Run:

docker run link-drop

---

🛠️ 14 — Troubleshooting

"IndentationError"

╔══════════════════════════════════════╗
║ ❌ PYTHON INDENTATION ERROR          ║
╠══════════════════════════════════════╣
║ Check spaces inside functions,      ║
║ conditions and loops.               ║
╚══════════════════════════════════════╝

"Client is already connected"

Usually means the same Pyrogram client is being started more than once.

Make sure your application doesn't repeatedly execute:

await bot.start()

after a partial startup failure.

"ImportError"

Verify that the imported function exists in the referenced module:

from plugins.downloader import start_download

Koyeb unhealthy

Check:

1. Application is listening on PORT
2. Health endpoint returns HTTP 200
3. bot.py starts successfully
4. Environment variables are present
5. No plugin syntax/import errors

---

📊 15 — Runtime Flow

┌─────────────────────────────────────────────────────┐
│                    USER REQUEST                     │
└────────────────────────┬────────────────────────────┘
                         ▼
                  🔗 URL RECEIVED
                         │
                         ▼
                 🆔 REQUEST CREATED
                         │
                         ▼
                🎛️ FORMAT BUTTONS
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
         🎬 VIDEO              📄 DOCUMENT
              │                     │
              └──────────┬──────────┘
                         ▼
                    🔐 VERIFY USER
                         │
                         ▼
                    📥 DOWNLOAD
                         │
                         ▼
                    📤 TELEGRAM
                         │
                         ▼
                      ✅ DONE

---

🧩 16 — Extensibility

The plugin structure makes it easy to add future modules:

plugins/
│
├── start.py
├── callbacks.py
├── downloader.py
├── cancel.py
│
├── history.py       ← future
├── queue.py         ← future
├── admin.py         ← future
├── settings.py      ← future
└── statistics.py    ← future

Possible future additions:

⚡ Download Queue
📊 Statistics
👑 Admin Panel
📜 Download History
⚙️ User Settings
📡 Progress Updates
🗃️ Database Storage

---

⚠️ 17 — Responsible Use

LINK-DROP is intended for legitimate downloads.

Only download content you are authorized to access or download.

Respect:

- Copyright
- Website terms
- Content licenses
- Telegram limits
- Service provider policies

---

📝 18 — License

This project is provided for educational and personal use.

You are responsible for how you deploy and use the software.

---

<div align="center">╔══════════════════════════════════════════════════╗
║                                                  ║
║                 ⚡ LINK-DROP                     ║
║                                                  ║
║          URL  ───────────────►  TELEGRAM         ║
║                                                  ║
║          Python • Pyrogram • Aiohttp             ║
║                                                  ║
╚══════════════════════════════════════════════════╝

Built for Telegram. Built for speed. ⚡

⭐ Star the repository if you find it useful.

</div>
