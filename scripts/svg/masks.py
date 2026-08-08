from dataclasses import dataclass

from scripts.animation.easing import Easings
from scripts.animation.smil import Animate


# ============================================================
# Animated Reveal Mask
# ============================================================

@dataclass
class SVGMaskReveal:
    """
    Animated SVG mask.

    Reveals an SVG element from one direction.

    Supported directions:

        top
        bottom
        left
        right

    The mask uses user-space coordinates so that
    its geometry matches the SVG document coordinates.
    """

    id: str

    x: float
    y: float

    width: float
    height: float

    direction: str = "left"

    duration: str = "0.22s"
    begin: str = "0s"

    easing = Easings.EASE_OUT

    # --------------------------------------------------------
    # Render
    # --------------------------------------------------------

    def render(self):

        # ====================================================
        # TOP -> BOTTOM
        # ====================================================

        if self.direction == "top":

            animation = Animate(
                attribute_name="height",
                from_value="0",
                to_value=str(self.height),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            return (
                f'<mask '
                f'id="{self.id}" '
                f'maskUnits="userSpaceOnUse" '
                f'maskContentUnits="userSpaceOnUse" '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.width}" '
                f'height="{self.height}">'
                
                f'<rect '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.width}" '
                f'height="0" '
                f'fill="white">'
                
                f'{animation.render()}'
                
                f'</rect>'
                
                f'</mask>'
            )

        # ====================================================
        # LEFT -> RIGHT
        # ====================================================

        if self.direction == "left":

            animation = Animate(
                attribute_name="width",
                from_value="0",
                to_value=str(self.width),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            return (
                f'<mask '
                f'id="{self.id}" '
                f'maskUnits="userSpaceOnUse" '
                f'maskContentUnits="userSpaceOnUse" '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.width}" '
                f'height="{self.height}">'
                
                f'<rect '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="0" '
                f'height="{self.height}" '
                f'fill="white">'
                
                f'{animation.render()}'
                
                f'</rect>'
                
                f'</mask>'
            )

        # ====================================================
        # BOTTOM -> TOP
        # ====================================================

        if self.direction == "bottom":

            move = Animate(
                attribute_name="y",
                from_value=str(
                    self.y + self.height
                ),
                to_value=str(self.y),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            grow = Animate(
                attribute_name="height",
                from_value="0",
                to_value=str(self.height),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            return (
                f'<mask '
                f'id="{self.id}" '
                f'maskUnits="userSpaceOnUse" '
                f'maskContentUnits="userSpaceOnUse" '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.width}" '
                f'height="{self.height}">'

                f'<rect '
                f'x="{self.x}" '
                f'y="{self.y + self.height}" '
                f'width="{self.width}" '
                f'height="0" '
                f'fill="white">'

                f'{move.render()}'
                f'{grow.render()}'

                f'</rect>'

                f'</mask>'
            )

        # ====================================================
        # RIGHT -> LEFT
        # ====================================================

        if self.direction == "right":

            move = Animate(
                attribute_name="x",
                from_value=str(
                    self.x + self.width
                ),
                to_value=str(self.x),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            grow = Animate(
                attribute_name="width",
                from_value="0",
                to_value=str(self.width),
                duration=self.duration,
                begin=self.begin,
                easing=self.easing,
            )

            return (
                f'<mask '
                f'id="{self.id}" '
                f'maskUnits="userSpaceOnUse" '
                f'maskContentUnits="userSpaceOnUse" '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.width}" '
                f'height="{self.height}">'

                f'<rect '
                f'x="{self.x + self.width}" '
                f'y="{self.y}" '
                f'width="0" '
                f'height="{self.height}" '
                f'fill="white">'

                f'{move.render()}'
                f'{grow.render()}'

                f'</rect>'

                f'</mask>'
            )

        raise ValueError(
            f"Unsupported mask direction: {self.direction}"
        )