import numpy as np

from PIL import Image

from scripts.utils.logger import logger


class PixelMatrix:

    """
    Converts a PIL image into a grayscale
    NumPy matrix.

    Output:

    ndarray(height, width)

    containing values

    0

    ↓

    255
    """

    def __init__(self):

        pass

    # ---------------------------------------------

    def process(

        self,

        image: Image.Image,

    ) -> np.ndarray:

        logger.info("Generating Pixel Matrix")

        rgba = image.convert("RGBA")
        gray = rgba.convert("L")
        pixels = np.array(gray, dtype=np.uint8,)

        logger.info(f"Pixel Matrix : {pixels.shape[0]} rows × {pixels.shape[1]} cols")

        return pixels