from scripts.svg.bounding_box import BoundingBoxCalculator
from scripts.svg.typography import Typography


class SVGLayout:

    def __init__(self, typography=None):

        if typography is None:
            typography = Typography()

        self.typography = typography
        self.bounding_box = BoundingBoxCalculator()

    # ------------------------------------------------

    def calculate(self, matrix):

        box = self.bounding_box.process(matrix)
        padding = self.typography.padding

        width = (box.width * self.typography.glyph_width + padding * 2)
        height = (box.height * self.typography.glyph_height + padding * 2)

        return {
            "box": box,
            "width": width,
            "height": height,
            "padding": padding,
        }