import asyncio
import logging
import os

from aiohttp import web
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


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


# ============================================================
# Koyeb Health Server
# ============================================================

async def health(request):
    return web.Response(
        text="OK",
        status=200
    )


async def start_health_server():

    app = web.Application()

    app.router.add_get(
        "/",
        health
    )

    app.router.add_get(
        "/health",
        health
    )

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


# ============================================================
# Main
# ============================================================

async def main():

    logger.info("Starting Telegram bot...")

    bot = Bot()

    health_runner = await start_health_server()

    try:

        await bot.start()

        me = await bot.get_me()

        logger.info("=" * 40)
        logger.info("Bot Started Successfully")
        logger.info("Username: @%s", me.username)
        logger.info("ID: %s", me.id)
        logger.info("=" * 40)

        # Keep running
        await asyncio.Event().wait()

    except asyncio.CancelledError:

        pass

    except Exception:

        logger.exception(
            "Fatal error while running bot"
        )

    finally:

        logger.info("Stopping bot...")

        try:
            await bot.stop()
        except Exception:
            pass

        try:
            await health_runner.cleanup()
        except Exception:
            pass

        logger.info("Bot stopped.")


if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info(
            "Shutdown requested."
        )
