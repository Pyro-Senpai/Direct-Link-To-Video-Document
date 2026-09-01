import os
import logging

from PIL import Image

from config import DOWNLOAD_DIR


logger = logging.getLogger(__name__)


def create_thumbnail(
    filepath,
    width=320,
    height=320
):
    try:
        if not filepath:
            return None

        if not os.path.exists(filepath):
            return None

        image = Image.open(filepath)

        image.thumbnail(
            (width, height),
            Image.Resampling.LANCZOS
        )

        thumbnail_path = os.path.join(
            DOWNLOAD_DIR,
            f"thumb_{os.path.basename(filepath)}.jpg"
        )

        if image.mode not in (
            "RGB",
            "L"
        ):
            image = image.convert("RGB")

        image.save(
            thumbnail_path,
            "JPEG",
            quality=90
        )

        return thumbnail_path

    except Exception as error:
        logger.exception(
            "Thumbnail creation failed: %s",
            error
        )

        return None
