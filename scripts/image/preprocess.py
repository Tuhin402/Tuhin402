from pathlib import Path

from PIL import Image

from config.settings import (
    GENERATED_IMAGES,
    SAVE_DEBUG_IMAGES,
    TARGET_SIZE,
)

from scripts.image.cropper import ImageCropper
from scripts.image.filters import ImageFilters
from scripts.image.resizer import ImageResizer

from scripts.utils.logger import logger


class ImagePreprocessor:

    """
    Responsible for the complete image pipeline.

    Loader is NOT part of this class.

    Input:
        PIL Image

    Output:
        Normalized PIL Image
    """

    def __init__(self):

        self.cropper = ImageCropper()

        self.filters = ImageFilters()

        self.resizer = ImageResizer()

    # --------------------------------------------------

    def save_debug(
        self,
        image: Image.Image,
        filename: str,
    ):

        if not SAVE_DEBUG_IMAGES:
            return

        path = GENERATED_IMAGES / filename

        image.save(path)

        logger.info(f"Saved -> {filename}")

    # --------------------------------------------------

    def process(
        self,
        image: Image.Image,
    ) -> Image.Image:

        logger.info("Starting Image Pipeline")

        # --------------------------

        cropped = self.cropper.process(image)

        self.save_debug(
            cropped,
            "cropped.png",
        )

        # --------------------------

        filtered = self.filters.process(cropped)

        self.save_debug(
            filtered,
            "filtered.png",
        )

        # --------------------------

        normalized = self.resizer.resize_square(
            filtered,
            TARGET_SIZE,
        )

        self.save_debug(
            normalized,
            "normalized.png",
        )

        logger.info("Image Pipeline Complete")

        return normalized