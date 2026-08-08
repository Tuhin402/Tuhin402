from PIL import Image

from config.settings import CROP_PADDING
from scripts.utils.logger import logger


class ImageCropper:

    """
    Handles cropping and canvas preparation.
    """

    def __init__(self, padding=CROP_PADDING):
        self.padding = padding

    # --------------------------------------------------

    def auto_crop(self, image: Image.Image) -> Image.Image:
        """
        Crop away fully transparent pixels.
        """

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        alpha = image.getchannel("A")

        bbox = alpha.getbbox()

        if bbox is None:
            logger.warning("Image has no visible pixels.")
            return image

        left, top, right, bottom = bbox

        left = max(0, left - self.padding)
        top = max(0, top - self.padding)

        right = min(image.width, right + self.padding)
        bottom = min(image.height, bottom + self.padding)

        cropped = image.crop((left, top, right, bottom))

        logger.info(
            f"Cropped image : {cropped.width}x{cropped.height}"
        )

        return cropped

    # --------------------------------------------------

    def square_canvas(
        self,
        image: Image.Image,
        background=(0, 0, 0, 0),
    ) -> Image.Image:
        """
        Places image on a centered square canvas.
        """

        width, height = image.size

        canvas_size = max(width, height)

        canvas = Image.new(
            "RGBA",
            (canvas_size, canvas_size),
            background,
        )

        offset_x = (canvas_size - width) // 2
        offset_y = (canvas_size - height) // 2

        canvas.paste(
            image,
            (offset_x, offset_y),
            image,
        )

        logger.info(
            f"Square canvas : {canvas.width}x{canvas.height}"
        )

        return canvas

    # --------------------------------------------------

    def process(self, image: Image.Image) -> Image.Image:

        image = self.auto_crop(image)

        image = self.square_canvas(image)

        return image