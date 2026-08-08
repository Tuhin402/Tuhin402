from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps

from scripts.utils.logger import logger


class ImageFilters:

    """
    Handles every image enhancement step.
    Every function returns a NEW image.
    Nothing is modified in-place.
    """

    def __init__(
        self,
        gamma=0.90,
        sharpen_radius=2,
        sharpen_percent=180,
        sharpen_threshold=2,
    ):

        self.gamma = gamma

        self.sharpen_radius = sharpen_radius

        self.sharpen_percent = sharpen_percent

        self.sharpen_threshold = sharpen_threshold

    # --------------------------------------------------

    def autocontrast(
        self,
        image: Image.Image,
    ) -> Image.Image:

        logger.info("Applying auto contrast")

        return ImageOps.autocontrast(image)

    # --------------------------------------------------

    def gamma_correction(
        self,
        image: Image.Image,
    ) -> Image.Image:

        logger.info(f"Gamma correction ({self.gamma})")

        gamma = self.gamma

        lut = [

            int(
                pow(i / 255.0, gamma) * 255
            )

            for i in range(256)

        ]

        return image.point(lut)

    # --------------------------------------------------

    def sharpen(
        self,
        image: Image.Image,
    ) -> Image.Image:

        logger.info("Applying unsharp mask")

        return image.filter(

            ImageFilter.UnsharpMask(

                radius=self.sharpen_radius,

                percent=self.sharpen_percent,

                threshold=self.sharpen_threshold,

            )

        )

    # --------------------------------------------------

    def smooth(
        self,
        image: Image.Image,
    ) -> Image.Image:

        logger.info("Applying smoothing")

        return image.filter(

            ImageFilter.SMOOTH_MORE

        )

    # --------------------------------------------------

    def process(self, image: Image.Image,) -> Image.Image:

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        alpha = image.getchannel("A")

        rgb = image.convert("RGB")

        gray = ImageOps.grayscale(rgb)

        gray = ImageOps.autocontrast(gray)

        gray = self.gamma_correction(gray)

        gray = self.sharpen(gray)

        gray = self.smooth(gray)

        result = Image.merge("RGBA",(gray, gray, gray, alpha,),)

        return result