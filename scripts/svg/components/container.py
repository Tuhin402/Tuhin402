from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGRect

from scripts.animation.smil import AnimateOpacity
from scripts.animation.easing import Easings


# ============================================================
# SVG Container
# ============================================================

class SVGContainer(SVGComponent):
    """
    Holds multiple SVG components.

    Responsible only for composition.

    It does NOT render XML.

    It only collects SVGElements
    from child components.
    """

    def __init__(self):

        super().__init__()

        self.children = []

    # -------------------------------------------------

    def add(
        self,
        component,
    ):

        self.children.append(
            component
        )

        return self

    # -------------------------------------------------

    def clear(self):

        self.children.clear()

    # -------------------------------------------------

    def render(self):

        elements = []

        for component in self.children:

            rendered = component.render()

            if isinstance(
                rendered,
                list,
            ):

                elements.extend(
                    rendered
                )

            else:

                elements.append(
                    rendered
                )

        return elements


# ============================================================
# Visual Container
# ============================================================

class ContainerComponent(SVGComponent):
    """
    Draws the rounded background panel
    used by generated SVG documents.

    Geometry is supplied by the layout engine.

    The entrance animation is intentionally subtle
    and remains compatible with the shared SVG system.
    """

    DEFAULT_FILL = "#161B22"
    DEFAULT_STROKE = "#30363D"

    DEFAULT_STROKE_WIDTH = 1
    DEFAULT_RADIUS = 16

    # -------------------------------------------------

    def __init__(
        self,
        x,
        y,
        width,
        height,
        fill=DEFAULT_FILL,
        stroke=DEFAULT_STROKE,
        stroke_width=DEFAULT_STROKE_WIDTH,
        radius=DEFAULT_RADIUS,
        animation_begin="0s",
        animation_duration="0.25s",
    ):

        super().__init__()

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

        self.radius = radius

        self.animation_begin = (
            animation_begin
        )

        self.animation_duration = (
            animation_duration
        )

    # ============================================================
    # Render
    # ============================================================

    def render(self):

        element = SVGRect(

            x=self.x,
            y=self.y,

            width=self.width,
            height=self.height,

            fill=self.fill,

            stroke=self.stroke,
            stroke_width=self.stroke_width,

            rx=self.radius,
            ry=self.radius,

        )

        element.set_class(
            "pg-container"
        )

        element.set_opacity(0)

        element.animate(

            AnimateOpacity(

                begin=self.animation_begin,

                duration=self.animation_duration,

                easing=Easings.EASE_OUT,

            )

        )

        return [
            element
        ]
