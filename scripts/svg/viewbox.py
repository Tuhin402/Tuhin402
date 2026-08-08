from dataclasses import dataclass


@dataclass
class SVGViewBox:
    """
    Represents the responsive viewport
    for an SVG document.
    """

    width: float
    height: float

    x: float = 0
    y: float = 0

    preserve_aspect_ratio: str = "xMidYMid meet"

    @property
    def value(self):

        return (
            f"{self.x} "
            f"{self.y} "
            f"{self.width} "
            f"{self.height}"
        )


class SVGViewBoxEngine:
    """
    Calculates the final SVG viewport.
    """

    def build(
        self,
        width,
        height,
    ):

        return SVGViewBox(

            width=width,
            height=height,

        )