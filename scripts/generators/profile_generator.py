from config.settings import PROFILE_IMAGE

from scripts.generators.base import BaseGenerator

from scripts.image.loader import ImageLoader
from scripts.image.preprocess import ImagePreprocessor

from scripts.ascii.alpha import AlphaMatrix
from scripts.ascii.dithering import FloydSteinbergDither
from scripts.ascii.matrix import ASCIIMatrix
from scripts.ascii.pixels import PixelMatrix
from scripts.ascii.renderer import ASCIIRenderer
from scripts.ascii.resolution import ASCIIResolution

from scripts.svg.renderer import SVGRenderer

from scripts.utils.logger import logger


class ProfileGenerator(BaseGenerator):
    """
    Generates the main ASCII profile SVG.

    The animated SVG is written to:

        generated/svg/ascii.svg

    The README generator references this SVG directly.
    """

    def __init__(self):

        self.loader = ImageLoader(
            PROFILE_IMAGE
        )

        self.preprocessor = (
            ImagePreprocessor()
        )

        self.resolution = (
            ASCIIResolution()
        )

        self.pixel_matrix = (
            PixelMatrix()
        )

        self.alpha_matrix = (
            AlphaMatrix()
        )

        self.dither = (
            FloydSteinbergDither()
        )

        self.ascii_matrix = (
            ASCIIMatrix()
        )

        self.preview = (
            ASCIIRenderer()
        )

        self.svg = (
            SVGRenderer()
        )

    # --------------------------------------------------

    def generate(self):

        logger.info("=" * 60)

        logger.info(
            "PROFILE GENERATOR"
        )

        logger.info("=" * 60)

        # ------------------------------------------------
        # Load source image
        # ------------------------------------------------

        image = self.loader.load()

        # ------------------------------------------------
        # Image preprocessing
        # ------------------------------------------------

        normalized = (
            self.preprocessor.process(
                image
            )
        )

        # ------------------------------------------------
        # ASCII resolution
        # ------------------------------------------------

        ascii_image = (
            self.resolution.process(
                normalized
            )
        )

        # ------------------------------------------------
        # Pixel matrix
        # ------------------------------------------------

        pixels = (
            self.pixel_matrix.process(
                ascii_image
            )
        )

        # ------------------------------------------------
        # Alpha matrix
        # ------------------------------------------------

        alpha = (
            self.alpha_matrix.process(
                ascii_image
            )
        )

        # ------------------------------------------------
        # Dithering
        # ------------------------------------------------

        pixels = (
            self.dither.process(
                pixels
            )
        )

        # ------------------------------------------------
        # ASCII matrix
        # ------------------------------------------------

        matrix = (
            self.ascii_matrix.process(
                pixels,
                alpha,
            )
        )

        # ------------------------------------------------
        # Save ASCII text / JSON
        # ------------------------------------------------

        self.preview.render(
            matrix
        )

        # ------------------------------------------------
        # Generate animated SVG
        # ------------------------------------------------

        self.svg.render(
            matrix
        )

        logger.info(
            "Profile generation complete."
        )