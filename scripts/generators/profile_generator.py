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
    """

    def __init__(self):

        self.loader = ImageLoader(PROFILE_IMAGE)
        self.preprocessor = ImagePreprocessor()
        self.resolution = ASCIIResolution()
        self.pixel_matrix = PixelMatrix()
        self.alpha_matrix = AlphaMatrix()
        self.dither = FloydSteinbergDither()
        self.ascii_matrix = ASCIIMatrix()
        self.preview = ASCIIRenderer()
        self.svg = SVGRenderer()

    # --------------------------------------------------

    def generate(self):

        logger.info("=" * 60)
        logger.info("PROFILE GENERATOR")
        logger.info("=" * 60)

        image = self.loader.load()

        normalized = self.preprocessor.process(image)
        ascii_image = self.resolution.process(normalized)
        pixels = self.pixel_matrix.process(ascii_image)
        alpha = self.alpha_matrix.process(ascii_image)
        pixels = self.dither.process(pixels)
        matrix = self.ascii_matrix.process(pixels, alpha,)

        self.preview.render(matrix)
        self.svg.render(matrix)

        logger.info("Profile generation complete.")