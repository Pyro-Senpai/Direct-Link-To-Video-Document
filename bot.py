import os
import logging
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN

# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Bot Client
# --------------------------------------------------

class LinkDownloaderBot(Client):

    def __init__(self):
        super().__init__(
            name="link_downloader_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(
                root="plugins"
            ),
            workers=16
        )

    async def start(self):
        await super().start()

        me = await self.get_me()

        logger.info(
            "========================================"
        )
        logger.info(
            "Bot Started Successfully"
        )
        logger.info(
            "Username: @%s",
            me.username
        )
        logger.info(
            "ID: %s",
            me.id
        )
        logger.info(
            "========================================"
        )

    async def stop(self, *args):
        logger.info("Stopping bot...")

        await super().stop()

        logger.info("Bot stopped.")


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    try:
        app = LinkDownloaderBot()

        logger.info("Starting Telegram bot...")

        app.run()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")

    except Exception as e:
        logger.exception(
            "Fatal error while running bot: %s",
            e
        )
