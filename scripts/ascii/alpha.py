import numpy as np

from PIL import Image

from scripts.utils.logger import logger


class AlphaMatrix:

    """
    Extracts the alpha channel
    from an RGBA image.
    """

    def process(

        self,

        image: Image.Image,

    ):

        logger.info(

            "Generating Alpha Matrix"

        )

        if image.mode != "RGBA":

            image = image.convert("RGBA")

        alpha = np.array(

            image.getchannel("A"),

            dtype=np.uint8,

        )

        logger.info(

            f"Alpha Matrix : {alpha.shape[0]} × {alpha.shape[1]}"

        )

        return alpha