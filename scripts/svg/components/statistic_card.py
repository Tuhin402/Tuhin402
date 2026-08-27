from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGRect
from scripts.svg.elements import SVGText

from scripts.svg.typography import Typography
from scripts.svg.theme import DEFAULT_THEME

from scripts.animation.smil import (
    AnimateOpacity,
    AnimateTransform,
)
from scripts.animation.easing import Easings


class StatisticCardComponent(SVGComponent):
    """
    Reusable statistic card.

    The card keeps the existing visual structure and theme,
    while supporting a subtle entrance animation.

    Animation sequence:

        Card background
            ↓
        Title
            ↓
        Value

    The animation is intentionally subtle and does not
    behave like a scanner.
    """

    def __init__(
        self,
        title,
        value,
        x,
        y,
        width=180,
        height=90,
        typography=None,
        theme=None,
        animation_begin="0s",
    ):

        super().__init__()

        self.title = str(title).upper()
        self.value = str(value)

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.typography = typography or Typography()
        self.theme = theme or DEFAULT_THEME

        # -------------------------------------------------
        # Animation timing
        # -------------------------------------------------

        self.animation_begin = animation_begin

    # =====================================================
    # Value formatting
    # =====================================================

    def _display_value(self):
        """
        Prevent extremely long values from
        overflowing the card.
        """

        maximum = 16

        if len(self.value) <= maximum:
            return self.value

        return self.value[:13] + "..."

    # -----------------------------------------------------

    def _value_font_size(self):

        length = len(self.value)

        if length <= 6:
            return 28

        if length <= 10:
            return 24

        if length <= 14:
            return 20

        if length <= 18:
            return 18

        return 16

    # =====================================================
    # Animation helpers
    # =====================================================

    def _animation_time(
        self,
        offset,
    ):
        """
        Adds a small deterministic offset to the
        card's main animation start time.

        Example:

            0.40s + 0.08s
            -> 0.48s
        """

        value = float(
            self.animation_begin.rstrip("s")
        )

        return f"{value + offset:.3f}s"

    # -----------------------------------------------------

    def _fade_animation(
        self,
        begin,
        duration="0.24s",
    ):
        """
        Creates the standard opacity reveal.
        """

        return AnimateOpacity(
            begin=begin,
            duration=duration,
            easing=Easings.EASE_OUT,
        )

    # -----------------------------------------------------

    def _rise_animation(
        self,
        begin,
        distance=6,
        duration="0.28s",
    ):
        """
        Creates a subtle upward movement.

        The element starts slightly below its final
        position and settles into place.
        """

        return AnimateTransform(
            transform_type="translate",
            from_value=f"0 {distance}",
            to_value="0 0",
            begin=begin,
            duration=duration,
            easing=Easings.EASE_OUT,
        )

    # =====================================================
    # Render
    # =====================================================

    def render(self):

        elements = []

        # =================================================
        # Card Background
        # =================================================

        background = SVGRect(

            x=self.x,
            y=self.y,

            width=self.width,
            height=self.height,

            fill=self.theme.card_background,

            rx=12,
            ry=12,

        )

        background.set_class("pg-stat-card")

        # -------------------------------------------------
        # Initially hidden.
        #
        # This prevents the card from being visible before
        # its SMIL animation begins.
        # -------------------------------------------------

        background.set_opacity(0)

        # -------------------------------------------------
        # Background fade
        # -------------------------------------------------

        background.animate(
            self._fade_animation(
                begin=self.animation_begin,
                duration="0.26s",
            )
        )

        # -------------------------------------------------
        # Background rise
        # -------------------------------------------------

        background.animate(
            self._rise_animation(
                begin=self.animation_begin,
                distance=7,
                duration="0.30s",
            )
        )

        elements.append(background)

        # =================================================
        # Title
        # =================================================

        title = SVGText(

            x=self.x + 16,
            y=self.y + 24,

            value=self.title,

            fill=self.theme.subtitle,

            font_family=self.typography.font_family,

            font_size=13,

            font_weight="600",

        )

        title.set_class("pg-stat-title")

        # -------------------------------------------------
        # Title starts shortly after the card begins.
        # -------------------------------------------------

        title_begin = self._animation_time(
            0.08
        )

        title.set_opacity(0)

        title.animate(
            self._fade_animation(
                begin=title_begin,
                duration="0.20s",
            )
        )

        title.animate(
            self._rise_animation(
                begin=title_begin,
                distance=3,
                duration="0.22s",
            )
        )

        elements.append(title)

        # =================================================
        # Value
        # =================================================

        value = SVGText(

            x=self.x + 16,
            y=self.y + 60,

            value=self._display_value(),

            fill=self.theme.title,

            font_family=self.typography.font_family,

            font_size=self._value_font_size(),

            font_weight="700",

        )

        value.set_class("pg-stat-value")

        # -------------------------------------------------
        # Value appears slightly after the title.
        # -------------------------------------------------

        value_begin = self._animation_time(
            0.15
        )

        value.set_opacity(0)

        value.animate(
            self._fade_animation(
                begin=value_begin,
                duration="0.24s",
            )
        )

        value.animate(
            self._rise_animation(
                begin=value_begin,
                distance=4,
                duration="0.26s",
            )
        )

        elements.append(value)

        return elements