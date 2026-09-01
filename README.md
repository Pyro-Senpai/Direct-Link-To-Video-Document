<div align="center">⚡ Telegram Link Downloader Bot

<p>A simple and powerful Telegram bot for downloading files from supported URLs and sending them directly to Telegram.</p><p>
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Pyrogram-2.x-2CA5E0?style=for-the-badge">
  <img src="https://img.shields.io/badge/Aiohttp-Async-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Koyeb-Ready-purple?style=for-the-badge">
</p></div><br><div align="center"><table>
<tr>
<td align="center">🔗 Simple

Send a URL and choose the required format.

</td>
<td align="center">⚡ Fast

Built with asynchronous Python.

</td>
<td align="center">🔒 Secure

User-specific callback requests.

</td>
</tr>
</table></div>---

✨ Features

<div align="center"><table>
<tr>
<td>🔗 Direct URL Downloads</td>
<td>🎬 Video Support</td>
</tr>
<tr>
<td>📄 Document Support</td>
<td>❌ Cancel Downloads</td>
</tr>
<tr>
<td>🆔 Temporary Request IDs</td>
<td>🔒 User Verification</td>
</tr>
<tr>
<td>⚡ Async Processing</td>
<td>🌐 Health Server</td>
</tr>
<tr>
<td>☁️ Koyeb Ready</td>
<td>🐳 Docker Support</td>
</tr>
</table></div>---

🔄 How It Works

<div align="center">User
  ↓
Send URL
  ↓
Bot Creates Request
  ↓
Choose Format
  ↓
Download
  ↓
Send File to Telegram

</div>---

📂 Project Structure

<div>
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

</div>

🧩 Architecture

<div align="center"><table>
<tr>
<th>File</th>
<th>Purpose</th>
</tr>
<tr>
<td><code>bot.py</code></td>
<td>Starts the bot and health server</td>
</tr>
<tr>
<td><code>config.py</code></td>
<td>Environment configuration</td>
</tr>
<tr>
<td><code>start.py</code></td>
<td>Handles start command and URLs</td>
</tr>
<tr>
<td><code>callbacks.py</code></td>
<td>Handles Video / Document buttons</td>
</tr>
<tr>
<td><code>downloader.py</code></td>
<td>Download engine</td>
</tr>
<tr>
<td><code>cancel.py</code></td>
<td>Handles download cancellation</td>
</tr>
</table></div>---

🔐 Callback Security

Instead of putting the complete URL inside Telegram's callback data, the bot generates a short temporary ID.

<div align="center"><table>
<tr>
<td>Original URL

"https://example.com/video.mp4"

</td>
<td>→</td>
<td>Temporary ID

"a91f42c8d301"

</td>
<td>→</td>
<td>Callback

"video:a91f42c8d301"

</td>
</tr>
</table></div>The bot stores:

Short ID
   ↓
User ID
   ↓
Download URL

Before downloading, the bot verifies that the button belongs to the correct user.

---

🎛️ Download Options

<div align="center"><table>
<tr>
<td align="center">🎬 Video

Send the downloaded file as a Telegram video.

</td>
<td align="center">📄 Document

Send the downloaded file as a Telegram document.

</td>
</tr>
</table><br>🎬 Video| 📄 Document
Video output| File output
Telegram video| Telegram document

</div>---

⚙️ Requirements

<div align="center"><table>
<tr>
<td>Python 3.10+</td>
<td>Telegram Bot</td>
</tr>
<tr>
<td>API ID</td>
<td>API Hash</td>
</tr>
</table></div>Main packages:

Pyrogram
Pyrofork
Pyromod
Aiohttp
Aiofiles
TgCrypto

---

🔑 Configuration

Set these environment variables:

API_ID=YOUR_API_ID
API_HASH=YOUR_API_HASH
BOT_TOKEN=YOUR_BOT_TOKEN

<div align="center">«⚠️ Never publish your "BOT_TOKEN" or "API_HASH".»

</div>---

💻 Local Installation

1. Clone

git clone YOUR_REPOSITORY_URL
cd LINK-DOWNLOADER

2. Install Dependencies

pip install -r requirements.txt

3. Start Bot

python bot.py

---

☁️ Koyeb Deployment

<div align="center"><table>
<tr>
<td align="center">1️⃣ Repository

Connect your GitHub repository to Koyeb.

</td>
<td align="center">2️⃣ Variables

Add your Telegram credentials.

</td>
<td align="center">3️⃣ Deploy

Deploy the service and wait for health checks.

</td>
</tr>
</table></div>Environment Variables

API_ID
API_HASH
BOT_TOKEN

Start Command

python bot.py

Health Endpoints

/
 /health

Both endpoints return:

OK

---

🐳 Docker

Build

docker build -t telegram-link-downloader .

Run

docker run telegram-link-downloader

---

🩺 Health Server

The bot includes an "aiohttp" server for cloud deployment health checks.

<div align="center"><table>
<tr>
<th>Endpoint</th>
<th>Response</th>
</tr>
<tr>
<td><code>/</code></td>
<td>HTTP 200 — OK</td>
</tr>
<tr>
<td><code>/health</code></td>
<td>HTTP 200 — OK</td>
</tr>
</table></div>The server uses the "PORT" environment variable and falls back to "8080".

---

🛠️ Troubleshooting

"IndentationError"

Check the indentation inside functions, loops and conditions.

Correct:

async def example():
    print("Hello")

"ImportError"

Verify that the required function exists in the referenced plugin.

from plugins.downloader import start_download

"Client is already connected"

This happens when the same Pyrogram client is started more than once.

Make sure you do not repeatedly call:

await bot.start()

on an already-connected client.

Koyeb Health Check Failed

Check:

<div align="center"><table>
<tr>
<td>✓</td>
<td>Application listens on <code>0.0.0.0</code></td>
</tr>
<tr>
<td>✓</td>
<td><code>PORT</code> is configured correctly</td>
</tr>
<tr>
<td>✓</td>
<td>Health endpoint returns HTTP 200</td>
</tr>
<tr>
<td>✓</td>
<td>Environment variables are present</td>
</tr>
<tr>
<td>✓</td>
<td>No Python syntax/import errors</td>
</tr>
</table></div>---

🛡️ Security

<div align="center"><table>
<tr>
<td>🔐</td>
<td><b>Keep credentials private</b></td>
</tr>
<tr>
<td>🚫</td>
<td>Never commit secrets to GitHub</td>
</tr>
<tr>
<td>🔑</td>
<td>Use environment variables</td>
</tr>
<tr>
<td>♻️</td>
<td>Regenerate exposed bot tokens</td>
</tr>
</table></div>---

🚧 Roadmap

<div align="center"><table>
<tr>
<td>✅ Core Downloader</td>
<td>✅ Video / Document</td>
</tr>
<tr>
<td>✅ Cancel System</td>
<td>✅ Callback Security</td>
</tr>
<tr>
<td>✅ Koyeb Support</td>
<td>⬜ Download Progress</td>
</tr>
<tr>
<td>⬜ Download Queue</td>
<td>⬜ Download History</td>
</tr>
<tr>
<td>⬜ Admin Panel</td>
<td>⬜ Statistics</td>
</tr>
</table></div>---

⚠️ Disclaimer

This project is intended for educational and legitimate use.

Only download content that you are authorized to access. Respect copyright laws and the terms of service of the websites and services you use.

---

📜 License

This project is provided for educational and personal use.

See the repository license for the applicable terms.

---

<div align="center">⚡ LINK-DROP

Built with Python • Pyrogram • Aiohttp

<br>⭐ Star the repository if you find it useful.

</div>
