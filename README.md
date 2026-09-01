<p align="center">
  <a href="#!">
    <img src="YOUR_BANNER_URL" alt="Telegram Link Downloader Bot Banner" width="100%" />
  </a>
</p><h1 align="center">🤖 Telegram Link Downloader Bot</h1><p align="center">
  <b>A fast, modern and secure Telegram link downloader built with Python, Pyrogram and Aiohttp.</b>
</p><p align="center">
  <a href="#!">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=111111" alt="Python">
  </a>
  <a href="#!">
    <img src="https://img.shields.io/badge/Pyrogram-2.x-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&labelColor=111111" alt="Pyrogram">
  </a>
  <a href="#!">
    <img src="https://img.shields.io/badge/Aiohttp-Async-orange?style=for-the-badge&labelColor=111111" alt="Aiohttp">
  </a>
  <a href="#!">
    <img src="https://img.shields.io/badge/Koyeb-Ready-8B5CF6?style=for-the-badge&logo=koyeb&logoColor=white&labelColor=111111" alt="Koyeb">
  </a>
</p><p align="center">
  <a href="#features">✨ Features</a> •
  <a href="#installation">⚙️ Installation</a> •
  <a href="#configuration">🔐 Configuration</a> •
  <a href="#deployment">🚀 Deployment</a>
</p><hr>📡 System Overview

<p align="center">
  <img src="https://img.shields.io/badge/BOT_STATUS-ONLINE-00E676?style=flat-square&labelColor=111111" alt="Bot Status">
  <img src="https://img.shields.io/badge/ASYNC-ENABLED-00E5FF?style=flat-square&labelColor=111111" alt="Async">
  <img src="https://img.shields.io/badge/KOYEB-READY-8B5CF6?style=flat-square&labelColor=111111" alt="Koyeb">
</p>Graph TD

    User[👤 Telegram User]

    Bot[🤖 Link Downloader Bot]

    URL[🔗 URL Handler]

    Format{📦 Choose Format}

    Video[🎬 Video]

    Document[📄 Document]

    Downloader[⚡ Download Engine]

    Telegram[💬 Telegram]

    Cancel[❌ Cancel Download]

    Health[🌐 Aiohttp Health Server]

    Koyeb[☁️ Koyeb]

    User -->|Send URL| Bot
    Bot --> URL
    URL --> Format

    Format -->|Video| Video
    Format -->|Document| Document

    Video --> Downloader
    Document --> Downloader

    Downloader -->|Upload| Telegram
    Telegram -->|Result| User

    User -->|Cancel| Cancel
    Cancel --> Downloader

    Koyeb --> Health
    Health --> Koyeb

<hr>⚡ Features

<div align="center"><table>
<tr>
<td align="center" width="33%">🔗 URL Downloader

Send a supported direct URL and start the download process.

</td><td align="center" width="33%">🎬 Video Mode

Send downloaded content as a Telegram video.

</td><td align="center" width="33%">📄 Document Mode

Send downloaded content as a Telegram document.

</td>
</tr><tr>
<td align="center">🆔 Secure Request ID

Full URLs are not stored inside callback data.

</td><td align="center">🔒 User Verification

Download buttons are restricted to their creator.

</td><td align="center">❌ Cancel System

Users can cancel an active download.

</td>
</tr><tr>
<td align="center">⚡ Async Engine

Built around Python's asynchronous architecture.

</td><td align="center">🌐 Health Server

Aiohttp server for cloud health checks.

</td><td align="center">🔄 FloodWait Handling

Automatically waits when Telegram applies FloodWait.

</td>
</tr>
</table></div><hr>🔄 Download Flow

sequenceDiagram

    participant U as 👤 User
    participant B as 🤖 Bot
    participant D as ⚡ Downloader
    participant T as 💬 Telegram

    U->>B: Send URL
    B->>B: Create temporary request ID
    B-->>U: Show Video / Document buttons

    U->>B: Select format
    B->>B: Verify User ID
    B->>D: Start download

    D->>D: Download file
    D->>T: Upload file
    T-->>U: Send downloaded file

<hr>🔐 Secure Callback System

The bot avoids placing the complete URL inside "callback_data".

Instead, it generates a temporary identifier.

<div align="center"><table>
<tr>
<th>Stage</th>
<th>Example</th>
</tr><tr>
<td>🔗 Original URL</td>
<td><code>https://example.com/video.mp4</code></td>
</tr><tr>
<td>🆔 Request ID</td>
<td><code>a91f42c8d301</code></td>
</tr><tr>
<td>🎬 Callback</td>
<td><code>video:a91f42c8d301</code></td>
</tr>
</table></div>The request internally contains:

Request ID
    ↓
Telegram User ID
    ↓
Download URL

Before starting a download, the bot checks whether the callback belongs to the same Telegram user who created the request.

<hr>🎛️ Download Controls

<div align="center"><table>
<tr><td align="center" width="50%">🎬 VIDEO

🎬 Video

Downloads and sends the file using the selected video mode.

</td><td align="center" width="50%">📄 DOCUMENT

📄 Document

Downloads and sends the file as a Telegram document.

</td></tr><tr><td colspan="2" align="center">❌ CANCEL

❌ Cancel

Stops an active download when supported by the downloader.

</td></tr>
</table></div><hr>📂 Project Structure

<div align="center"><table>
<tr>
<th>📄 File / Folder</th>
<th>🎯 Purpose</th>
</tr><tr>
<td><code>bot.py</code></td>
<td>🤖 Main bot entry point, Pyrogram client and Koyeb health server.</td>
</tr><tr>
<td><code>config.py</code></td>
<td>🔐 Telegram API and bot configuration.</td>
</tr><tr>
<td><code>requirements.txt</code></td>
<td>📦 Python dependencies required by the project.</td>
</tr><tr>
<td><code>Dockerfile</code></td>
<td>🐳 Docker container configuration.</td>
</tr><tr>
<td><code>README.md</code></td>
<td>📖 Project documentation and setup guide.</td>
</tr><tr>
<td><code>plugins/</code></td>
<td>🧩 Modular Telegram bot handlers.</td>
</tr><tr>
<td><code>plugins/start.py</code></td>
<td>🚀 Handles the <code>/start</code> command and URL messages.</td>
</tr><tr>
<td><code>plugins/callbacks.py</code></td>
<td>🎛️ Handles Video, Document and Cancel callback buttons.</td>
</tr><tr>
<td><code>plugins/downloader.py</code></td>
<td>⚡ Handles file downloading and Telegram uploading.</td>
</tr><tr>
<td><code>plugins/cancel.py</code></td>
<td>❌ Handles download cancellation functionality.</td>
</tr></table></div>

<hr>🧩 Module Architecture

<div align="center"><table><tr>
<th>Module</th>
<th>Responsibility</th>
</tr><tr>
<td><code>bot.py</code></td>
<td>Starts Pyrogram and the Koyeb health server.</td>
</tr><tr>
<td><code>config.py</code></td>
<td>Stores Telegram configuration values.</td>
</tr><tr>
<td><code>plugins/start.py</code></td>
<td>Handles the start command and URL input.</td>
</tr><tr>
<td><code>plugins/callbacks.py</code></td>
<td>Handles Video, Document and Cancel callbacks.</td>
</tr><tr>
<td><code>plugins/downloader.py</code></td>
<td>Contains the download and upload logic.</td>
</tr><tr>
<td><code>plugins/cancel.py</code></td>
<td>Handles cancellation-related functionality.</td>
</tr></table></div><hr>🛠 Requirements

<div align="center"><table>
<tr>
<td>🐍 Python</td>
<td>3.10+</td>
</tr><tr>
<td>🤖 Telegram Bot</td>
<td>Bot Token</td>
</tr><tr>
<td>🔑 Telegram API</td>
<td>API ID + API Hash</td>
</tr><tr>
<td>☁️ Cloud</td>
<td>Optional — Koyeb / VPS / Docker</td>
</tr>
</table></div>Python Packages

Pyrogram
Pyromod
Aiohttp
Aiofiles
TgCrypto

<hr>🔐 Configuration

Set the following environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

<div align="center"><table>
<tr>
<th>Variable</th>
<th>Purpose</th>
</tr><tr>
<td><code>API_ID</code></td>
<td>Telegram API identifier.</td>
</tr><tr>
<td><code>API_HASH</code></td>
<td>Telegram API hash.</td>
</tr><tr>
<td><code>BOT_TOKEN</code></td>
<td>Telegram bot authentication token.</td>
</tr>
</table></div>«⚠️ Never upload your API credentials or bot token to a public repository.»

<hr>⚙️ Installation

1️⃣ Clone Repository

git clone YOUR_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Configure Environment

Set:

API_ID
API_HASH
BOT_TOKEN

4️⃣ Start Bot

python bot.py

<hr>🚀 Deployment

☁️ Koyeb

The project contains a built-in Aiohttp health server.

0.0.0.0:$PORT

Default fallback:

8080

Health endpoints:

/
 /health

Both return:

OK

<div align="center"><table>
<tr><td align="center">1️⃣ Repository

Connect your GitHub repository.

</td><td align="center">2️⃣ Environment

Add your Telegram credentials.

</td><td align="center">3️⃣ Deploy

Start the service and wait for health checks.

</td></tr>
</table></div>Start Command

python bot.py

<hr>🐳 Docker

Build

docker build -t telegram-link-downloader .

Run

docker run telegram-link-downloader

<hr>🌐 Health Monitoring

Graph LR

    K[☁️ Koyeb]
    H[🌐 Aiohttp]
    P[8080 / $PORT]
    OK[✅ HTTP 200 OK]

    K --> H
    H --> P
    P --> OK

    style K fill:#312e81,stroke:#8b5cf6,color:#fff
    style H fill:#164e63,stroke:#06b6d4,color:#fff
    style P fill:#422006,stroke:#f59e0b,color:#fff
    style OK fill:#14532d,stroke:#22c55e,color:#fff

<hr>🩺 Troubleshooting

<details>
<summary><b>❌ IndentationError</b></summary><br><table>Make sure every function body is correctly indented.

async def example():
    print("Hello")</table>

</details><details>
<summary><b>❌ ImportError</b></summary><br>Check that the imported function actually exists in the target plugin.

Example:

from plugins.downloader import start_download

Make sure "start_download" is defined inside:

plugins/downloader.py

</details><details>
<summary><b>❌ Client is already connected</b></summary><br>This usually happens when the same Pyrogram client is started more than once.

Avoid repeatedly calling:

await bot.start()

on an already-connected client.

</details><details>
<summary><b>❌ Koyeb Health Check Failed</b></summary><br>Check the following:

- Application listens on "0.0.0.0"
- "$PORT" is used
- "/" returns HTTP "200"
- Environment variables are configured
- Dependencies install successfully
- No Python syntax errors exist

</details><hr>🔒 Security Checklist

<div align="center"><table><tr>
<td>🔑</td>
<td>Keep <code>BOT_TOKEN</code> private.</td>
</tr><tr>
<td>🛡️</td>
<td>Keep <code>API_HASH</code> private.</td>
</tr><tr>
<td>🚫</td>
<td>Never commit secrets to GitHub.</td>
</tr><tr>
<td>♻️</td>
<td>Regenerate an exposed bot token immediately.</td>
</tr><tr>
<td>👤</td>
<td>Validate the callback user before starting downloads.</td>
</tr></table></div><hr>🧭 Roadmap

<div align="center"><table><tr>
<td>✅ URL Handler</td>
<td>✅ Video Mode</td>
<td>✅ Document Mode</td>
</tr><tr>
<td>✅ Callback Security</td>
<td>✅ Cancel Button</td>
<td>✅ Koyeb Health Server</td>
</tr><tr>
<td>⬜ Download Progress</td>
<td>⬜ Queue System</td>
<td>⬜ Download History</td>
</tr><tr>
<td>⬜ Admin Controls</td>
<td>⬜ Statistics</td>
<td>⬜ Database Support</td>
</tr></table></div><hr>⚠️ Disclaimer

<div align="center">This project is intended for educational and legitimate purposes.

Only download files and content that you are authorized to access.
Please respect copyright laws and the terms of service of the services you use.

</div><hr>❤️ Credits

<p align="center"><b>Built with Python & Pyrogram</b>

<br><br>

⚡ Fast • 🔒 Secure • 🧩 Modular • ☁️ Cloud Ready

<br><br>

⭐ <b>If you find this project useful, consider starring the repository.</b>

</p><div align="center"><img src="https://img.shields.io/badge/Made%20With-❤️-red?style=for-the-badge&labelColor=111111">
<img src="https://img.shields.io/badge/Open%20Source-✓-success?style=for-the-badge&labelColor=111111"></div>
