from PIL import Image

from config.settings import ASCII_WIDTH

from scripts.utils.logger import logger


class ASCIIResolution:
    """
    Converts the normalized portrait into
    the optimal resolution for ASCII rendering.

    Terminal characters are significantly taller
    than they are wide, so we compensate during
    resizing to preserve the original portrait
    proportions.
    """

    def __init__(
        self,
        width=ASCII_WIDTH,
        character_aspect_ratio=0.55,
    ):

        self.width = width

        # Height correction factor.
        # 0.50 ~ 0.60 generally works well for
        # monospaced fonts like JetBrains Mono.
        self.character_aspect_ratio = character_aspect_ratio

        self.resample = Image.Resampling.LANCZOS

    # -------------------------------------------------

    def process(
        self,
        image: Image.Image,
    ):

        original_width, original_height = image.size

        image_ratio = (
            original_height
            / original_width
        )

        new_height = max(
            1,
            round(
                image_ratio
                * self.width
                * self.character_aspect_ratio
            ),
        )

        logger.info(
            "ASCII Resolution : "
            f"{self.width} × {new_height}"
        )

        resized = image.resize(
            (
                self.width,
                new_height,
            ),
            self.resample,
        )

        return resized