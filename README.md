<div align="center">⚡ LINK⚡DROP

"Telegram Link Downloader"

Turn direct links into Telegram files — fast, simple & clean.

<br>""Python" (https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)" (https://www.python.org/)
""Pyrogram" (https://img.shields.io/badge/Pyrogram-2.x-2CA5E0?style=flat-square)" (https://docs.pyrogram.org/)
""Aiohttp" (https://img.shields.io/badge/Aiohttp-Async-2C3E50?style=flat-square)" (https://docs.aiohttp.org/)
""Koyeb" (https://img.shields.io/badge/Koyeb-Ready-7C3AED?style=flat-square)" (https://www.koyeb.com/)

</div>---

"01" — WHAT IS LINK⚡DROP?

«LINK⚡DROP is an asynchronous Telegram downloader bot designed to receive a downloadable URL, process it, and return the file directly to the user.»

       ┌───────────────────────────────┐
       │        🔗  DIRECT URL          │
       └───────────────┬───────────────┘
                       │
                       ▼
       ┌───────────────────────────────┐
       │        🤖  TELEGRAM BOT        │
       └───────────────┬───────────────┘
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      ┌─────────────┐     ┌─────────────┐
      │ 🎬  VIDEO   │     │ 📄 DOCUMENT │
      └──────┬──────┘     └──────┬──────┘
             │                   │
             └─────────┬─────────┘
                       ▼
              ┌─────────────────┐
              │ 📤 TELEGRAM FILE │
              └─────────────────┘

---

"02" — CORE FEATURES

<table>
<tr>
<td width="50%">🎬 Dual Format

Send downloads as:

- Video
- Document

</td>
<td width="50%">⚡ Async Engine

Built around asynchronous Python for efficient processing.

</td>
</tr><tr>
<td>🔒 Request Protection

Each download request receives a unique short ID and is tied to the requesting Telegram user.

</td>
<td>❌ Smart Cancel

Users can cancel an active download directly from the inline keyboard.

</td>
</tr><tr>
<td>☁️ Koyeb Ready

Includes an HTTP health server for cloud deployment and health checks.

</td>
<td>🧩 Plugin Architecture

Features are separated into individual plugin modules for easier maintenance.

</td>
</tr>
</table>---

"03" — USER FLOW

┌──────────────┐
│ 👤 USER      │
└──────┬───────┘
       │
       │  Send URL
       ▼
┌──────────────────────┐
│ 🤖 LINK⚡DROP         │
│ Request received     │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────┐
│ 📥 Choose download format  │
├─────────────┬──────────────┤
│ 🎬 VIDEO    │ 📄 DOCUMENT  │
└─────────────┴──────────────┘
           │
           ▼
┌──────────────────────┐
│      📥 DOWNLOAD     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      📤 TELEGRAM     │
└──────────────────────┘

---

"04" — BUTTON SYSTEM

The bot generates a temporary request ID instead of placing the complete URL inside Telegram's callback data.

┌─────────────────────────────────────────┐
│       📥 CHOOSE DOWNLOAD FORMAT         │
├──────────────────────┬──────────────────┤
│     🎬 VIDEO         │   📄 DOCUMENT    │
├──────────────────────┴──────────────────┤
│              ❌ CANCEL                   │
└─────────────────────────────────────────┘

Example callback:

video:a91f42c8d301

instead of:

video:https://example.com/a/very/long/download/url

---

"05" — PROJECT MAP

LINK⚡DROP/
│
├── 🤖 bot.py
│   └── Application entry point
│
├── ⚙️ config.py
│   └── Environment configuration
│
├── 📦 requirements.txt
│   └── Python dependencies
│
├── 🐳 Dockerfile
│   └── Container configuration
│
├── 📖 README.md
│
└── 🧩 plugins/
    │
    ├── 🚀 start.py
    │   └── Start command & URL handling
    │
    ├── 🎛️ callbacks.py
    │   └── Video / Document / Cancel buttons
    │
    ├── 📥 downloader.py
    │   └── Download engine
    │
    └── ❌ cancel.py
        └── Cancel command

---

"06" — ENVIRONMENT

Create these environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

🔐 Keep Secrets Private

┌──────────────────────────────────────┐
│ ⚠️ NEVER COMMIT THESE TO GITHUB      │
├──────────────────────────────────────┤
│ API_HASH                             │
│ BOT_TOKEN                            │
│ DATABASE_URL  (if used)              │
└──────────────────────────────────────┘

Use Koyeb environment variables or a local ".env" setup instead.

---

"07" — LOCAL SETUP

Clone

git clone YOUR_REPOSITORY_URL
cd LINK-DOWNLOADER

Install

pip install -r requirements.txt

Run

python bot.py

Expected startup:

┌──────────────────────────────────────┐
│ 🚀 Starting Telegram bot...          │
│                                      │
│ 🌐 Health server started             │
│ 🤖 Bot Started Successfully          │
└──────────────────────────────────────┘

---

"08" — KOYEB DEPLOYMENT

GitHub
   │
   ▼
┌───────────────┐
│     KOYEB     │
├───────────────┤
│ Build          │
│ Deploy         │
│ Health Check   │
└───────┬───────┘
        │
        ▼
   🤖 BOT ONLINE

Required Variables

API_ID
API_HASH
BOT_TOKEN

Start Command

python bot.py

The included health server listens on Koyeb's "PORT" environment variable, falling back to "8080".

---

"09" — HEALTH CHECK

Endpoints:

GET /
GET /health

Response:

OK

Example:

┌─────────────────────────────────┐
│ Koyeb Health Check              │
├─────────────────────────────────┤
│ GET /                           │
│                                 │
│ HTTP 200                        │
│ Response: OK                    │
└─────────────────────────────────┘

---

"10" — ERROR HANDLING

FloodWait

Telegram "FloodWait" errors are handled automatically with a delay before retrying.

Startup Errors

Fatal startup errors are allowed to terminate the process rather than repeatedly calling "bot.start()" on an already-connected Pyrogram client.

Error
  │
  ├── FloodWait ──► Wait ──► Retry
  │
  └── Other Error ──► Stop ──► Koyeb Restart

---

"11" — REQUIREMENTS

Typical dependencies:

Pyrogram
Pyrofork
Pyromod
Aiohttp
Aiofiles
TgCrypto

Use the versions defined in your project's actual "requirements.txt".

---

"12" — SECURITY MODEL

Each URL request follows:

URL
 │
 ▼
Generate UUID
 │
 ▼
Short ID
 │
 ▼
Store:
 ├── User ID
 └── URL
 │
 ▼
Inline Button
 │
 ▼
User clicks
 │
 ▼
Verify User ID
 │
 ▼
Start Download

If another Telegram user attempts to use the button:

❌ This button belongs to another user.

---

"13" — DISCLAIMER

This project is intended for legitimate downloads and educational purposes.

Only download content that you are authorized to access and download. Respect the terms of service and copyright laws applicable to the content and service you use.

---

<div align="center">⚡ LINK⚡DROP

Simple URL → Telegram.

Built with Python • Pyrogram • Aiohttp

⭐ Star the project if you find it useful.

</div>
