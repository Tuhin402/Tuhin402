from PIL import Image

from scripts.utils.logger import logger


class ImageResizer:

    """
    Responsible for every resize operation.

    Always preserves quality.

    Uses Lanczos resampling.
    """

    def __init__(self):

        self.resample = Image.Resampling.LANCZOS

    # --------------------------------------------------

    def resize(
        self,
        image: Image.Image,
        width: int,
        height: int,
    ) -> Image.Image:

        logger.info(
            f"Resize -> {width}x{height}"
        )

        return image.resize(
            (width, height),
            self.resample,
        )

    # --------------------------------------------------

    def resize_square(
        self,
        image: Image.Image,
        size: int,
    ) -> Image.Image:

        logger.info(
            f"Square Resize -> {size}"
        )

        return image.resize(
            (size, size),
            self.resample,
        )

    # --------------------------------------------------

    def resize_width(
        self,
        image: Image.Image,
        width: int,
    ) -> Image.Image:

        old_width, old_height = image.size

        ratio = width / old_width

        height = int(old_height * ratio)

        logger.info(
            f"Resize Width -> {width}"
        )

        return image.resize(
            (width, height),
            self.resample,
        )

    # --------------------------------------------------

    def resize_height(
        self,
        image: Image.Image,
        height: int,
    ) -> Image.Image:

        old_width, old_height = image.size

        ratio = height / old_height

        width = int(old_width * ratio)

        logger.info(
            f"Resize Height -> {height}"
        )

        return image.resize(
            (width, height),
            self.resample,
        )

    # --------------------------------------------------

    def thumbnail(
        self,
        image: Image.Image,
        max_size: int,
    ) -> Image.Image:

        copy = image.copy()

        copy.thumbnail(
            (max_size, max_size),
            self.resample,
        )

        logger.info(
            f"Thumbnail -> {copy.size}"
        )

        return copy