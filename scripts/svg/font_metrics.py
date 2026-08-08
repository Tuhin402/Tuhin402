from fontTools.ttLib import TTFont

from scripts.utils.logger import logger


class FontMetrics:
    """
    Reads accurate glyph metrics from
    a TrueType/OpenType font.

    The renderer relies on the advance
    width of a normal monospace glyph,
    not the maximum glyph in the font.
    """

    def __init__(self, font_path):

        logger.info(f"Loading Font : {font_path.name}")

        self.font = TTFont(font_path)

        self.head = self.font["head"]
        self.hhea = self.font["hhea"]
        self.hmtx = self.font["hmtx"]
        self.cmap = self.font.getBestCmap()

    # ------------------------------------------------

    @property
    def units_per_em(self):

        return self.head.unitsPerEm

    # ------------------------------------------------

    def _glyph_advance(self):

        """
        Returns the advance width of a
        representative monospace glyph.

        Preference order:

        M
        0
        space

        Falls back to advanceWidthMax.
        """

        for character in ("M", "0", " "):

            codepoint = ord(character)

            glyph_name = self.cmap.get(codepoint)

            if glyph_name and glyph_name in self.hmtx.metrics:

                advance, _ = self.hmtx.metrics[glyph_name]
                return advance

        logger.warning(
            "Falling back to advanceWidthMax."
        )

        return self.hhea.advanceWidthMax

    # ------------------------------------------------

    def glyph_width(self, font_size):

        advance = self._glyph_advance()

        width = (
            advance
            / self.units_per_em
        ) * font_size

        logger.info(
            f"Glyph Width : {width:.3f}"
        )

        return width