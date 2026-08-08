from dataclasses import dataclass
from typing import Optional


# ============================================================
# Base Definition
# ============================================================

@dataclass
class SVGDefinition:
    """
    Base class for everything that belongs
    inside the <defs> section.
    """

    id: str

    def render(self) -> str:
        raise NotImplementedError


# ============================================================
# Clip Path
# ============================================================

@dataclass
class SVGClipPath(SVGDefinition):
    """
    Generic rectangular clipPath.

    More shapes can be added later.
    """

    x: float
    y: float

    width: float
    height: float

    rx: float = 0
    ry: float = 0

    def render(self):

        return (
            f'<clipPath id="{self.id}">'
            f'<rect '
            f'x="{self.x}" '
            f'y="{self.y}" '
            f'width="{self.width}" '
            f'height="{self.height}" '
            f'rx="{self.rx}" '
            f'ry="{self.ry}"'
            f' />'
            f'</clipPath>'
        )


# ============================================================
# Mask
# ============================================================

@dataclass
class SVGMask(SVGDefinition):
    """
    Generic rectangular SVG mask.

    White = visible

    Black = hidden

    Gray = partial opacity.
    """

    x: float
    y: float

    width: float
    height: float

    fill: str = "white"

    def render(self):

        return (
            f'<mask id="{self.id}">'
            f'<rect '
            f'x="{self.x}" '
            f'y="{self.y}" '
            f'width="{self.width}" '
            f'height="{self.height}" '
            f'fill="{self.fill}"'
            f' />'
            f'</mask>'
        )