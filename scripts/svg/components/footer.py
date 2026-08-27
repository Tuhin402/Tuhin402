from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGText

from scripts.svg.typography import Typography
from scripts.svg.theme import DEFAULT_THEME

from scripts.animation.smil import AnimateOpacity
from scripts.animation.easing import Easings


class FooterComponent(SVGComponent):
    """
    Renders a reusable footer.

    The footer remains intentionally quiet so it does not
    compete with the primary data visualizations.
    """

    FONT_SIZE = 12

    ANIMATION_DURATION = "0.18s"

    def __init__(
        self,
        text: str,
        x: float,
        y: float,
        typography=None,
        theme=None,
        animation_begin="1.30s",
    ):

        super().__init__()

        self.text = text

        self.x = x
        self.y = y

        self.typography = (
            typography
            or Typography()
        )

        self.theme = (
            theme
            or DEFAULT_THEME
        )

        self.animation_begin = (
            animation_begin
        )

    # ========================================================
    # Render
    # ========================================================

    def render(self):

        element = SVGText(

            x=self.x,
            y=self.y,

            value=self.text,

            fill=self.theme.subtitle,

            font_family=(
                self.typography.font_family
            ),

            font_size=self.FONT_SIZE,

            font_weight="400",

        )

        element.set_class(
            "pg-footer"
        )

        element.set_opacity(0)

        element.animate(

            AnimateOpacity(

                begin=self.animation_begin,

                duration=self.ANIMATION_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        return [
            element
        ]
