# Telegram Direct Link Downloader Bot

A modular Telegram bot that downloads files from direct URLs and sends them back to the user as either a **Video** or **Document**.

## ✨ Features

- 🔗 Direct URL downloader
- 🎬 Send files as Telegram Video
- 📁 Send files as Telegram Document
- 📊 Download progress
- ⚡ Download speed
- ⏱️ ETA
- ❌ Cancel active downloads
- 🗑️ Automatic temporary-file cleanup
- 💾 MongoDB user database
- 📜 Download history
- 📦 4 GB application download limit
- 🐳 Docker support
- 🚀 Koyeb-ready
- 🔌 Modular plugin structure
- 👥 Multiple users
- 🔒 Short IDs for callback buttons

> Audio/MP3 functionality is intentionally not included.

---

# 📁 Project Structure

```text
telegram-link-bot/
│
├── bot.py
├── config.py
├── Dockerfile
├── Procfile
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── database/
│   ├── __init__.py
│   └── database.py
│
├── plugins/
│   ├── __init__.py
│   ├── start.py
│   ├── downloader.py
│   ├── callbacks.py
│   └── cancel.py
│
└── downloads/
    └── .gitkeep
