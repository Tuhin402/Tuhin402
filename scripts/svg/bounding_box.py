from dataclasses import dataclass
from scripts.utils.logger import logger


@dataclass
class BoundingBox:
    """
    Represents the visible region
    of an ASCII matrix.
    """

    min_x: int
    min_y: int
    max_x: int
    max_y: int

    @property
    def width(self):

        return self.max_x - self.min_x + 1

    @property
    def height(self):

        return self.max_y - self.min_y + 1

    @property
    def center_x(self):

        return self.min_x + self.width / 2

    @property
    def center_y(self):

        return self.min_y + self.height / 2


class BoundingBoxCalculator:

    """
    Finds the visible ASCII bounds.
    Ignores spaces.
    """

    def process(self, matrix):

        logger.info("Calculating ASCII Bounding Box")

        rows = len(matrix)
        cols = len(matrix[0])

        min_x = cols
        min_y = rows

        max_x = -1
        max_y = -1

        for y in range(rows):

            for x in range(cols):

                if matrix[y][x] == " ":
                    continue

                min_x = min(min_x, x)
                min_y = min(min_y, y)

                max_x = max(max_x, x)
                max_y = max(max_y, y)

        if max_x == -1:

            logger.warning("ASCII matrix is empty.")

            return BoundingBox(0,0,0,0,)

        box = BoundingBox(
            min_x,
            min_y,
            max_x,
            max_y,
        )

        logger.info(
            f"Bounding Box : "
            f"({box.min_x},{box.min_y}) "
            f"→ "
            f"({box.max_x},{box.max_y})"
        )

        logger.info(f"Visible Size : " f"{box.width} × {box.height}")

        return box