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

logger = logging.getLogger(__name__)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="link_downloader_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={
                "root": "plugins"
            },
        )


async def health(request):
    return web.Response(
        text="OK",
        status=200,
    )


async def start_health_server():

    app = web.Application()

    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)

    await runner.setup()

    port = int(
        os.environ.get("PORT", "8080")
    )

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port,
    )

    await site.start()

    logger.info(
        "Health server started on port %s",
        port,
    )

    return runner


async def start_bot(bot):

    try:

        logger.info("Connecting to Telegram...")

        await bot.start()

        logger.info(
            "Telegram connection successful."
        )

        return True

    except FloodWait as e:

        wait_time = int(e.value) + 5

        logger.warning(
            "Telegram FloodWait detected."
        )

        logger.warning(
            "Waiting %s seconds before retrying...",
            wait_time,
        )

        await asyncio.sleep(wait_time)

        return False

    except Exception:

        logger.exception(
            "Failed to start Telegram bot."
        )

        raise


async def main():

    logger.info("Starting Telegram bot...")

    health_runner = await start_health_server()

    bot = Bot()

    bot_started = False

    try:

        while not bot_started:

            bot_started = await start_bot(bot)

            if not bot_started:

                logger.info(
                    "Retrying Telegram bot connection..."
                )

        me = await bot.get_me()

        logger.info("=" * 50)
        logger.info("BOT STARTED SUCCESSFULLY")
        logger.info("Username: @%s", me.username)
        logger.info("ID: %s", me.id)
        logger.info("=" * 50)

        await asyncio.Event().wait()

    except asyncio.CancelledError:

        logger.info(
            "Bot task cancelled."
        )

    except KeyboardInterrupt:

        logger.info(
            "Shutdown requested."
        )

    except Exception:

        logger.exception(
            "Fatal error while running bot."
        )

        raise

    finally:

        if bot_started:

            try:

                logger.info(
                    "Stopping Telegram bot..."
                )

                await bot.stop()

            except Exception:

                logger.exception(
                    "Error while stopping Telegram bot."
                )

        try:

            logger.info(
                "Stopping health server..."
            )

            await health_runner.cleanup()

        except Exception:

            logger.exception(
                "Error while stopping health server."
            )

        logger.info(
            "Application stopped."
        )


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info(
            "Shutdown requested."
        )
