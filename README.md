<div align="center">⚡ LINK-DROP

Advanced Telegram Link Downloader

**"URL" → "PROCESS" → "DOWNLOAD" → "TELEGRAM"

<br>"Python" (https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
"Pyrogram" (https://img.shields.io/badge/Pyrogram-2.x-2CA5E0?style=for-the-badge)
"Aiohttp" (https://img.shields.io/badge/Aiohttp-Async-2C3E50?style=for-the-badge)
"Koyeb" (https://img.shields.io/badge/Koyeb-Ready-7C3AED?style=for-the-badge)
"Docker" (https://img.shields.io/badge/Docker-Supported-2496ED?style=for-the-badge&logo=docker&logoColor=white)

<br>⚡ Fast  •  🧩 Modular  •  🔒 Secure  •  ☁️ Cloud Ready

</div>---

<div align="center">╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                      ⚡ LINK-DROP                            ║
║                                                              ║
║              ADVANCED TELEGRAM DOWNLOADER                   ║
║                                                              ║
║          🔗 URL  ───────►  📥 FILE  ───────►  📤 TG         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

</div>🧠 About

LINK-DROP is an asynchronous Telegram downloader built with Python, Pyrogram and Aiohttp.

It is designed around a modular plugin architecture, temporary download requests, protected callback buttons and cloud-friendly health checks.

┌─────────────────────────────────────────────────────┐
│                    LINK-DROP                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  🔗 Receive URL                                     │
│       ↓                                             │
│  🆔 Create Request                                  │
│       ↓                                             │
│  🎛️ Choose Format                                  │
│       ↓                                             │
│  📥 Download                                        │
│       ↓                                             │
│  📤 Send to Telegram                                │
│                                                     │
└─────────────────────────────────────────────────────┘

---

✨ Feature Matrix

Feature| Status
🔗 URL Downloader| ✅
🎬 Video Output| ✅
📄 Document Output| ✅
❌ Cancel Download| ✅
🆔 Temporary Request ID| ✅
🔒 User Ownership Check| ✅
⚡ Async Architecture| ✅
🧩 Plugin System| ✅
🌐 Health Server| ✅
☁️ Koyeb Ready| ✅
🐳 Docker Support| ✅
🔄 FloodWait Handling| ✅
📱 Telegram Inline UI| ✅

---

🏗️ Architecture

                         TELEGRAM
                            │
                            ▼
                  ┌──────────────────┐
                  │    PYROGRAM      │
                  │    BOT CLIENT    │
                  └────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        ┌─────────┐   ┌──────────┐   ┌─────────┐
        │ START   │   │ CALLBACK │   │ CANCEL  │
        │ PLUGIN  │   │ PLUGIN   │   │ PLUGIN  │
        └────┬────┘   └────┬─────┘   └────┬────┘
             │             │              │
             └─────────────┼──────────────┘
                           ▼
                  ┌──────────────────┐
                  │    DOWNLOADER    │
                  │      ENGINE      │
                  └────────┬─────────┘
                           │
                           ▼
                    ┌────────────┐
                    │ FILE DATA  │
                    └─────┬──────┘
                          │
                          ▼
                    📤 TELEGRAM

---

📂 Project Structure

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

Module Responsibilities

┌──────────────────────────────────────────────────┐
│ bot.py                                           │
│ Application lifecycle + Koyeb health server     │
├──────────────────────────────────────────────────┤
│ config.py                                        │
│ Environment configuration                        │
├──────────────────────────────────────────────────┤
│ start.py                                         │
│ /start + URL handling                            │
├──────────────────────────────────────────────────┤
│ callbacks.py                                     │
│ Video / Document / Cancel callbacks              │
├──────────────────────────────────────────────────┤
│ downloader.py                                    │
│ Download execution                               │
├──────────────────────────────────────────────────┤
│ cancel.py                                        │
│ Active download cancellation                     │
└──────────────────────────────────────────────────┘

---

🔐 Request Security

LINK-DROP does not put the complete URL inside the callback data.

Instead, every request receives a temporary ID.

                 ORIGINAL URL
                      │
                      ▼
              ┌───────────────┐
              │ Generate UUID │
              └───────┬───────┘
                      │
                      ▼
                 SHORT ID
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
          USER ID             URL
             │                 │
             └────────┬────────┘
                      ▼
                INLINE BUTTON

Example:

video:a91f42c8d301

Instead of:

video:https://example.com/very/long/download/url/file.mp4

---

🛡️ User Verification

Every callback request is checked against the original user's Telegram ID.

┌──────────────────────┐
│ Button Clicked       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Find Request ID      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Compare User IDs     │
└──────────┬───────────┘
           │
       ┌───┴────┐
       │        │
      MATCH    FAIL
       │        │
       ▼        ▼
   DOWNLOAD   REJECT

Unauthorized users receive:

╔════════════════════════════════════╗
║ 🔒 ACCESS DENIED                   ║
╠════════════════════════════════════╣
║ ❌ This button belongs to          ║
║    another user.                   ║
╚════════════════════════════════════╝

---

🎛️ Interactive Downloader UI

After receiving a URL:

╔════════════════════════════════════════╗
║       📥 CHOOSE DOWNLOAD FORMAT        ║
╠════════════════════╦═══════════════════╣
║     🎬 VIDEO       ║   📄 DOCUMENT     ║
╠════════════════════╩═══════════════════╣
║              ❌ CANCEL                  ║
╚════════════════════════════════════════╝

🎬 Video

Uploads the result as a Telegram video.

📄 Document

Uploads the result as a Telegram document.

❌ Cancel

Attempts to stop the active download associated with the user.

---

🔄 Complete Request Lifecycle

┌───────────────┐
│ 👤 USER       │
│ Sends URL     │
└───────┬───────┘
        │
        ▼
┌───────────────────────┐
│ 🚀 URL HANDLER        │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 🆔 REQUEST MANAGER    │
│                       │
│ user_id + URL         │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 🎛️ FORMAT SELECTOR   │
└──────────┬────────────┘
           │
       ┌───┴────┐
       ▼        ▼
    VIDEO    DOCUMENT
       │        │
       └───┬────┘
           ▼
┌───────────────────────┐
│ 🔒 USER VALIDATION    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 📥 DOWNLOAD ENGINE    │
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│ 📤 TELEGRAM UPLOAD    │
└──────────┬────────────┘
           │
           ▼
        ✅ DONE

---

⚙️ Environment Configuration

Create these environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

If your downloader uses additional configuration, add those variables according to your project.

---

🔒 Secret Management

╔══════════════════════════════════════════════╗
║                  🔐 SECURITY                 ║
╠══════════════════════════════════════════════╣
║                                              ║
║ ❌ Never publish BOT_TOKEN                   ║
║ ❌ Never publish API_HASH                    ║
║ ❌ Never commit private credentials          ║
║                                              ║
║ ✅ Use environment variables                ║
║ ✅ Use Koyeb Secrets / Variables             ║
║ ✅ Keep local credentials outside Git        ║
║                                              ║
╚══════════════════════════════════════════════╝

---

🔑 Telegram Configuration

Create Bot

Open @BotFather and run:

/newbot

Copy the generated bot token.

Get API Credentials

Visit:

https://my.telegram.org/

Then:

Login
  ↓
API Development Tools
  ↓
Create New Application
  ↓
API ID + API HASH

---

🧪 Local Installation

Clone

git clone YOUR_REPOSITORY_URL
cd LINK-DROP

Install

pip install -r requirements.txt

Start

python bot.py

Expected startup:

╔══════════════════════════════════════════════╗
║              ⚡ LINK-DROP                   ║
╠══════════════════════════════════════════════╣
║ 🌐 Health Server : ONLINE                   ║
║ 🔌 Telegram      : CONNECTING               ║
║ 🤖 Bot           : STARTING                 ║
╚══════════════════════════════════════════════╝

---

📦 Requirements

Typical dependencies:

Pyrogram
Pyrofork
Pyromod
Aiohttp
Aiofiles
TgCrypto

Use the exact packages and versions defined by your own "requirements.txt".

---

☁️ Koyeb Deployment

             ┌─────────────┐
             │   GitHub    │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │    KOYEB    │
             ├─────────────┤
             │ Build       │
             │ Deploy      │
             │ Health      │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │  LINK-DROP  │
             │    ONLINE   │
             └─────────────┘

Deployment Checklist

┌──────────────────────────────────────────────┐
│              ☁️ KOYEB CHECKLIST              │
├──────────────────────────────────────────────┤
│                                              │
│ [✓] GitHub repository connected             │
│ [✓] API_ID configured                       │
│ [✓] API_HASH configured                     │
│ [✓] BOT_TOKEN configured                    │
│ [✓] PORT available                          │
│ [✓] Health endpoint configured              │
│ [✓] Start command configured                │
│                                              │
└──────────────────────────────────────────────┘

Start Command

python bot.py

---

🩺 Health Server

The bot includes an "aiohttp" health server for cloud platforms.

Endpoints

GET /
GET /health

Response

HTTP/1.1 200 OK

OK

Port Logic

             PORT
              │
              ▼
       ┌───────────────┐
       │ Environment?  │
       └───────┬───────┘
               │
          ┌────┴────┐
          │         │
         YES        NO
          │         │
          ▼         ▼
       PORT      8080

---

🐳 Docker Deployment

Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]

Build

docker build -t link-drop .

Run

docker run link-drop

---

🔄 Error Recovery

The application handles Telegram "FloodWait" separately from unexpected startup errors.

                    ERROR
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
        FLOODWAIT          OTHER ERROR
             │                 │
             ▼                 ▼
        WAIT + RETRY       LOG ERROR
                               │
                               ▼
                          PROCESS EXIT
                               │
                               ▼
                       CLOUD RESTART

This prevents a failed startup from repeatedly calling "bot.start()" on an already-connected Pyrogram client.

---

🐛 Troubleshooting

"IndentationError"

╔══════════════════════════════════════╗
║ ❌ INDENTATION ERROR                 ║
╠══════════════════════════════════════╣
║ Check indentation inside functions, ║
║ loops and conditional statements.   ║
╚══════════════════════════════════════╝

Example:

async def test():
    print("Correct")

---

"Client is already connected"

This usually means the same Pyrogram client is being started more than once.

Avoid repeatedly executing:

await bot.start()

on the same client instance after a partial startup failure.

---

"ImportError"

Example:

ImportError: cannot import name 'start_download'

Verify that the function exists:

from plugins.downloader import start_download

and that the file exists:

plugins/downloader.py

---

Koyeb Health Check Failure

Check:

1. Server listens on 0.0.0.0
2. Application uses PORT
3. / returns HTTP 200
4. Bot starts without Python errors
5. Environment variables exist
6. requirements.txt installs successfully

---

📈 Performance Model

┌───────────────────────────────────────────┐
│              ASYNC PIPELINE               │
├───────────────────────────────────────────┤
│                                           │
│ Telegram Event                            │
│       ↓                                   │
│ Async Handler                             │
│       ↓                                   │
│ Request Lookup                            │
│       ↓                                   │
│ Download Task                             │
│       ↓                                   │
│ Telegram Upload                           │
│                                           │
└───────────────────────────────────────────┘

The application is designed around asynchronous operations to avoid blocking the Telegram event loop during normal I/O operations.

---

🧩 Extensible Plugin System

The architecture makes it easy to add additional features.

plugins/
│
├── start.py
├── callbacks.py
├── downloader.py
├── cancel.py
│
├── admin.py          ← Future
├── queue.py          ← Future
├── history.py        ← Future
├── statistics.py     ← Future
├── settings.py       ← Future
└── progress.py       ← Future

Potential extensions:

👑 Admin Panel
📊 Statistics
📜 Download History
⚙️ User Settings
📡 Live Progress
📥 Download Queue
🗃️ Persistent Database
🚦 Rate Limiting

---

🗺️ Roadmap

╔══════════════════════════════════════════════╗
║                 🚧 ROADMAP                   ║
╠══════════════════════════════════════════════╣
║                                              ║
║ ✅ Core Downloader                           ║
║ ✅ Video / Document                          ║
║ ✅ Cancel System                             ║
║ ✅ Callback Security                         ║
║ ✅ Koyeb Health Server                       ║
║                                              ║
║ 🔲 Persistent Download History               ║
║ 🔲 Advanced Progress UI                      ║
║ 🔲 Queue Management                           ║
║ 🔲 Admin Dashboard                           ║
║ 🔲 Usage Statistics                          ║
║ 🔲 User Settings                             ║
║                                              ║
╚══════════════════════════════════════════════╝

---

🤝 Contributing

Contributions are welcome.

Fork
  ↓
Create Branch
  ↓
Make Changes
  ↓
Test
  ↓
Commit
  ↓
Pull Request

Example:

git checkout -b feature/my-feature
git add .
git commit -m "Add my feature"
git push origin feature/my-feature

Then open a Pull Request.

---

⚠️ Responsible Use

LINK-DROP is intended for legitimate downloads and educational purposes.

Only download content that you are authorized to access.

Respect:

Copyright
Terms of Service
Content Licenses
Telegram Policies
Service Provider Policies

Do not use the project to bypass access controls or security mechanisms.

---

📜 License

This project is provided for educational and personal use.

See the repository license for the applicable terms.

---

<div align="center">╔══════════════════════════════════════════════════════╗
║                                                      ║
║                    ⚡ LINK-DROP                       ║
║                                                      ║
║              URL ───────► TELEGRAM                  ║
║                                                      ║
║        Built with Python • Pyrogram • Aiohttp       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

⚡ Simple Input. Powerful Processing. Clean Output.

⭐ Star the repository if LINK-DROP helped you.

</div>
