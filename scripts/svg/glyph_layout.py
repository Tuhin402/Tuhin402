from dataclasses import dataclass

from scripts.svg.typography import Typography


@dataclass
class GlyphPosition:
    """
    Represents the starting position
    of one rendered ASCII row.
    """

    row: int

    x: float
    y: float


class GlyphLayout:
    """
    Calculates where the visible ASCII
    content should begin inside the SVG.

    The layout is based entirely on the
    visible bounding box produced by the
    BoundingBoxCalculator.
    """

    def __init__(self, typography=None):

        self.typography = typography or Typography()

    # -------------------------------------------------

    def rows(self, matrix, box):

        positions = []

        # ---------------------------------------------
        # Starting position
        # ---------------------------------------------

        start_x = self.typography.padding

        start_y = (
            self.typography.padding
            + self.typography.font_size
        )

        # ---------------------------------------------
        # Create one position per visible row
        # ---------------------------------------------

        for visible_row, matrix_row in enumerate(
            range(box.min_y, box.max_y + 1)
        ):

            positions.append(

                GlyphPosition(

                    row=matrix_row,

                    x=start_x,

                    y=(
                        start_y
                        + visible_row
                        * self.typography.glyph_height
                    ),

                )

            )

        return positions