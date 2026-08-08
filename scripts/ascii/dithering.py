import numpy as np

from scripts.utils.logger import logger


class FloydSteinbergDither:

    """
    Applies Floyd–Steinberg error diffusion
    to a grayscale pixel matrix.

    Input:
        ndarray(uint8)

    Output:
        ndarray(uint8)
    """

    def __init__(self, levels=64):

        self.levels = levels

    # -------------------------------------------------

    def quantize(self, value):

        step = 255 / (self.levels - 1)

        return round(value / step) * step

    # -------------------------------------------------

    def process(self, pixels):

        logger.info(
            "Applying Floyd–Steinberg Dithering"
        )

        pixels = pixels.astype(np.float32)

        height, width = pixels.shape

        for y in range(height):

            for x in range(width):

                old = pixels[y, x]

                new = self.quantize(old)

                pixels[y, x] = new

                error = old - new

                if x + 1 < width:
                    pixels[y, x + 1] += error * 7 / 16

                if y + 1 < height:

                    if x > 0:
                        pixels[y + 1, x - 1] += error * 3 / 16

                    pixels[y + 1, x] += error * 5 / 16

                    if x + 1 < width:
                        pixels[y + 1, x + 1] += error * 1 / 16

        pixels = np.clip(
            pixels,
            0,
            255,
        )

        logger.info("Dithering Complete")

        return pixels.astype(np.uint8)