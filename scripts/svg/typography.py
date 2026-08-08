from dataclasses import dataclass, field

from config.settings import JETBRAINS_MONO

from scripts.svg.font_metrics import FontMetrics


@dataclass
class Typography:
    """
    Central typography engine.

    Every SVG layout should derive text
    measurements from this class instead
    of using hard-coded values.
    """

    # -------------------------------------------------
    # Font
    # -------------------------------------------------

    font_family: str = "JetBrains Mono"
    font_weight: str = "400"

    # -------------------------------------------------
    # Master Scale
    # -------------------------------------------------

    ascii_scale: float = 1.0

    base_font_size: float = 8.0

    # -------------------------------------------------
    # Spacing
    # -------------------------------------------------

    line_height_ratio: float = 1.15

    letter_spacing_ratio: float = 0.0

    padding: int = 24

    # -------------------------------------------------
    # Colors
    # -------------------------------------------------

    foreground: str = "#FFFFFF"
    background: str = "#000000"

    # -------------------------------------------------

    metrics: FontMetrics = field(init=False, repr=False)

    # -------------------------------------------------

    def __post_init__(self):

        self.metrics = FontMetrics(JETBRAINS_MONO)

    # =================================================
    # Computed Font Size
    # =================================================

    @property
    def font_size(self):

        return self.base_font_size * self.ascii_scale

    # =================================================
    # Character Width
    # =================================================

    @property
    def glyph_width(self):

        return self.metrics.glyph_width(
            self.font_size,
        )

    # =================================================
    # Character Height
    # =================================================

    @property
    def glyph_height(self):

        return (
            self.font_size
            * self.line_height_ratio
        )

    # =================================================
    # SVG Letter Spacing
    # =================================================

    @property
    def letter_spacing(self):

        return (
            self.font_size
            * self.letter_spacing_ratio
        )

    # =================================================
    # Line Height (SVG em units)
    # =================================================

    @property
    def line_height(self):

        return self.line_height_ratio

    # =================================================
    # Helpers
    # =================================================

    def text_width(self, characters):

        """
        Estimated width of a line
        containing 'characters'
        glyphs.
        """

        if characters <= 0:
            return 0

        return (
            characters * self.glyph_width
        )

    def text_height(self, rows):

        """
        Estimated height of
        multiple ASCII rows.
        """

        if rows <= 0:
            return 0

        return rows * self.glyph_height