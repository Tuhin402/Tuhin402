from scripts.ascii.mapper import BrightnessMapper
from scripts.utils.logger import logger


class ASCIIMatrix:
    """
    Converts a brightness matrix and an alpha matrix
    into an ASCII matrix.
    """

    def __init__(self, mapper=None):

        if mapper is None:
            mapper = BrightnessMapper()

        self.mapper = mapper

    # ---------------------------------------------

    def process(self, pixels, alpha):

        logger.info("Generating ASCII Matrix")

        matrix = []

        for y in range(pixels.shape[0]):

            ascii_row = []

            for x in range(pixels.shape[1]):

                pixel = pixels[y][x]
                alpha_value = alpha[y][x]

                if alpha_value < 10:
                    ascii_row.append(" ")
                else:
                    ascii_row.append(
                        self.mapper.map_pixel(int(pixel))
                    )

            matrix.append(ascii_row)

        logger.info(
            f"ASCII Matrix : {len(matrix)} × {len(matrix[0])}"
        )

        return matrix