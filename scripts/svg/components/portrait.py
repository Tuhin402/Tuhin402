from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGTextBlock

from scripts.svg.glyph_layout import GlyphLayout

from scripts.svg.typography import Typography

from scripts.svg.bounding_box import BoundingBoxCalculator

from scripts.animation.smil import SMILAnimation
from scripts.animation.easing import Easings


class PortraitComponent(SVGComponent):
    """
    Renders an ASCII portrait as SVG elements.
    """

    def __init__(self, matrix, typography=None,):

        super().__init__()
        self.matrix = matrix
        self.typography = typography or Typography()
        self.layout = GlyphLayout(self.typography)

        self.bounding_box = BoundingBoxCalculator()

    # --------------------------------------------------

    def render(self):

        box = self.bounding_box.process(self.matrix)
        positions = self.layout.rows(self.matrix, box,)

        rows = []

        for row in self.matrix[box.min_y: box.max_y + 1]:

            visible = row[box.min_x: box.max_x + 1]
            rows.append("".join(visible))

        block = SVGTextBlock(

            x=positions[0].x,
            y=positions[0].y,

            rows=rows,
            fill=self.typography.foreground,

            font_family=self.typography.font_family,
            font_size=self.typography.font_size,
            line_height=self.typography.line_height,
            font_weight=self.typography.font_weight,
            letter_spacing=self.typography.letter_spacing,

        )

        block.animate(
            SMILAnimation(
                attribute_name="opacity",
                from_value="0",
                to_value="1",
                duration="1.8s",
                easing=Easings.EASE_OUT,
            )
        )

        return [block]