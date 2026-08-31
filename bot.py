import asyncio
import logging
import os

from aiohttp import web
from pyrogram import Client
from pyrogram.errors import FloodWait

from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(
level=logging.INFO,
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(name)

class Bot(Client):

def __init__(self):

    super().__init__(
        "link_downloader_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins={
            "root": "plugins"
        },
    )

============================================================

Koyeb Health Server

============================================================

async def health(request):
return web.Response(
text="OK",
status=200
)

async def start_health_server():

app = web.Application()

app.router.add_get("/", health)
app.router.add_get("/health", health)

runner = web.AppRunner(app)

await runner.setup()

port = int(
    os.environ.get(
        "PORT",
        "8080"
    )
)

site = web.TCPSite(
    runner,
    "0.0.0.0",
    port
)

await site.start()

logger.info(
    "Health server started on port %s",
    port
)

return runner

============================================================

Start Bot With FloodWait Handling

============================================================

async def start_bot(bot):

while True:

    try:

        await bot.start()

        return

    except FloodWait as e:

        wait_time = e.value + 5

        logger.warning(
            "FloodWait detected! Waiting %s seconds before retrying...",
            wait_time
        )

        await asyncio.sleep(
            wait_time
        )

    except Exception:

        logger.exception(
            "Error while starting bot. Retrying in 30 seconds..."
        )

        await asyncio.sleep(
            30
        )

============================================================

Main

============================================================

async def main():

logger.info("Starting Telegram bot...")

bot = Bot()

health_runner = await start_health_server()

try:

    await start_bot(bot)

    me = await bot.get_me()

    logger.info("=" * 40)
    logger.info("Bot Started Successfully")
    logger.info("Username: @%s", me.username)
    logger.info("ID: %s", me.id)
    logger.info("=" * 40)

    # Keep bot running forever
    await asyncio.Event().wait()

except asyncio.CancelledError:

    logger.info(
        "Bot task cancelled."
    )

except Exception:

    logger.exception(
        "Fatal error while running bot"
    )

finally:

    logger.info("Stopping bot...")

    try:

        if bot.is_connected:
            await bot.stop()

    except Exception:

        pass

    try:

        await health_runner.cleanup()

    except Exception:

        pass

    logger.info("Bot stopped.")

if name == "main":

try:

    asyncio.run(main())

except KeyboardInterrupt:

    logger.info(
        "Shutdown requested."
    )