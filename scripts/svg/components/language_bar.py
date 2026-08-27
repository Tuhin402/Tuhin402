from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGRect
from scripts.svg.elements import SVGText

from scripts.svg.typography import Typography
from scripts.svg.theme import DEFAULT_THEME

from scripts.animation.smil import Animate
from scripts.animation.smil import AnimateOpacity
from scripts.animation.easing import Easings


class LanguageBarComponent(SVGComponent):
    """
    Displays a language with
    a percentage progress bar.

    Animation:

        1. Language label fades in.
        2. Percentage fades in.
        3. Track fades in.
        4. Progress bar grows from left to right.

    The component does NOT decide when the row
    enters the document. That timing is supplied
    through animation_begin.
    """

    LABEL_SIZE = 14
    PERCENTAGE_SIZE = 13

    # --------------------------------------------------------
    # Animation
    # --------------------------------------------------------

    LABEL_DURATION = "0.18s"
    PERCENTAGE_DURATION = "0.18s"

    TRACK_DURATION = "0.16s"
    BAR_DURATION = "0.32s"

    # --------------------------------------------------------

    def __init__(
        self,
        language: str,
        percentage: float,
        x: float,
        y: float,
        width: int = 260,
        height: int = 12,
        typography=None,
        theme=None,
        animation_begin="0s",
    ):

        super().__init__()

        self.language = language

        self.percentage = max(
            0,
            min(
                100,
                percentage,
            ),
        )

        self.x = x
        self.y = y

        self.width = width
        self.height = height

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
    # Timing helpers
    # ========================================================

    def _offset(
        self,
        seconds,
    ):
        """
        Adds a small relative delay to the
        row's main animation start time.
        """

        try:

            begin = float(
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

            begin = 0.0

        return (
            f"{begin + seconds:.3f}s"
        )

    # ========================================================
    # Render
    # ========================================================

    def render(self):

        elements = []

        # ====================================================
        # Language label
        # ====================================================

        language_text = SVGText(

            x=self.x,

            y=self.y,

            value=self.language,

            fill=self.theme.title,

            font_family=(
                self.typography.font_family
            ),

            font_size=self.LABEL_SIZE,

            font_weight="600",

        )

        language_text.set_class("pg-language-label")

        language_text.set_opacity(0)

        language_text.animate(

            AnimateOpacity(

                begin=self.animation_begin,

                duration=self.LABEL_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        elements.append(
            language_text
        )

        # ====================================================
        # Percentage
        # ====================================================

        percentage_text = SVGText(

            x=(
                self.x
                + self.width
                - 42
            ),

            y=self.y,

            value=(
                f"{self.percentage:.1f}%"
            ),

            fill=self.theme.subtitle,

            font_family=(
                self.typography.font_family
            ),

            font_size=self.PERCENTAGE_SIZE,

        )

        percentage_text.set_class("pg-language-percentage")

        percentage_text.set_opacity(0)

        percentage_text.animate(

            AnimateOpacity(

                begin=self._offset(0.04),

                duration=self.PERCENTAGE_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        elements.append(
            percentage_text
        )

        # ====================================================
        # Background track
        # ====================================================

        bar_y = (
            self.y
            + 12
        )

        track = SVGRect(

            x=self.x,

            y=bar_y,

            width=self.width,

            height=self.height,

            fill=self.theme.border,

            rx=6,

            ry=6,

        )

        track.set_class("pg-language-track")

        track.set_opacity(0)

        track.animate(

            AnimateOpacity(

                begin=self._offset(0.06),

                duration=self.TRACK_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        elements.append(
            track
        )

        # ====================================================
        # Filled progress bar
        # ====================================================

        filled_width = (
            self.width
            * self.percentage
            / 100
        )

        # ----------------------------------------------------
        # IMPORTANT
        #
        # width is a native SVGRect property.
        #
        # Therefore the rectangle itself starts with:
        #
        #     width=0
        #
        # and SMIL changes that SAME attribute to the
        # calculated filled width.
        #
        # Do NOT use set_attribute("width", "0") here,
        # because that would create:
        #
        #     width="0"
        #     width="..."
        #
        # which produces invalid XML.
        # ----------------------------------------------------

        progress = SVGRect(

            x=self.x,

            y=bar_y,

            width=0,

            height=self.height,

            fill=self.theme.accent,

            rx=6,

            ry=6,

        )

        progress.set_class("pg-language-progress")

        progress.animate(

            Animate(

                attribute_name="width",

                from_value="0",

                to_value=(
                    f"{filled_width:.3f}"
                ),

                begin=self._offset(0.08),

                duration=self.BAR_DURATION,

                easing=Easings.EASE_OUT,

            )

        )

        elements.append(
            progress
        )

        return elements