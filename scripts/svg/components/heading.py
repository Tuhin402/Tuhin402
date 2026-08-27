from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGText

from scripts.svg.typography import Typography
from scripts.svg.theme import DEFAULT_THEME

from scripts.animation.smil import AnimateOpacity
from scripts.animation.easing import Easings


class HeadingComponent(SVGComponent):
    """
    Reusable heading component.

    Supports:
        - title only
        - title + subtitle

    The generator controls when the heading begins;
    this component controls the internal title/subtitle
    choreography.
    """

    TITLE_SIZE = 16
    SUBTITLE_SIZE = 12

    TITLE_SPACING = 22
    SUBTITLE_SPACING = 18

    TITLE_ANIMATION_DURATION = "0.22s"
    SUBTITLE_ANIMATION_DURATION = "0.18s"

    SUBTITLE_ANIMATION_OFFSET = 0.08

    # --------------------------------------------------------

    def __init__(
        self,
        text=None,
        title=None,
        subtitle=None,
        x=0,
        y=0,
        typography=None,
        theme=None,
        animation_begin="0.10s",
    ):

        super().__init__()

        if title is None:
            title = text

        self.title = (
            title or ""
        ).upper()

        self.subtitle = subtitle

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
    # Height
    # ========================================================

    @property
    def height(self):

        if self.subtitle:

            return (
                self.TITLE_SIZE
                + self.TITLE_SPACING
                + self.SUBTITLE_SIZE
            )

        return self.TITLE_SIZE

    # ========================================================
    # Subtitle timing
    # ========================================================

    def _subtitle_begin(self):

        try:

            value = float(
                str(
                    self.animation_begin
                ).replace(
                    "s",
                    "",
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            value = 0.0

        return (
            f"{value + self.SUBTITLE_ANIMATION_OFFSET:.3f}s"
        )

    # ========================================================
    # Render
    # ========================================================

    def render(self):

        elements = []

        # ====================================================
        # Main Title
        # ====================================================

        title = SVGText(

            x=self.x,
            y=self.y,

            value=self.title,

            fill=self.theme.title,

            font_family=(
                self.typography.font_family
            ),

            font_size=self.TITLE_SIZE,

            font_weight="700",

            letter_spacing=1.5,

        )

        title.set_class(
            "pg-heading-title"
        )

        title.set_opacity(0)

        title.animate(

            AnimateOpacity(

                begin=self.animation_begin,

                duration=self.TITLE_ANIMATION_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        elements.append(title)

        # ====================================================
        # Subtitle
        # ====================================================

        if self.subtitle:

            subtitle = SVGText(

                x=self.x,

                y=(
                    self.y
                    + self.TITLE_SPACING
                ),

                value=self.subtitle,

                fill=self.theme.subtitle,

                font_family=(
                    self.typography.font_family
                ),

                font_size=self.SUBTITLE_SIZE,

                font_weight="400",

                letter_spacing=0,

            )

            subtitle.set_class(
                "pg-heading-subtitle"
            )

            subtitle.set_opacity(0)

            subtitle.animate(

                AnimateOpacity(

                    begin=self._subtitle_begin(),

                    duration=self.SUBTITLE_ANIMATION_DURATION,

                    easing=Easings.EASE_OUT,

                )

            )

            elements.append(subtitle)

        return elements
