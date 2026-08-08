import base64
from pathlib import Path

from scripts.utils.logger import logger


class SVGFontEngine:
    """
    Loads and embeds fonts
    directly into SVG.
    """

    def __init__(
        self,
        font_path,
        font_family="JetBrains Mono",
    ):

        self.font_path = Path(font_path)

        self.font_family = font_family

    # -------------------------------------

    def load(self):

        logger.info(
            f"Loading Font : {self.font_path.name}"
        )

        return self.font_path.read_bytes()

    # -------------------------------------

    def encode(self):

        font = self.load()

        encoded = base64.b64encode(
            font
        ).decode("utf8")

        logger.info(
            "Font Encoded"
        )

        return encoded

    # -------------------------------------

    def generate_style(self):

        encoded = self.encode()

        return f"""
<style>

@font-face {{

font-family:'{self.font_family}';

src:url(data:font/ttf;base64,{encoded}) format('truetype');

}}

</style>
"""