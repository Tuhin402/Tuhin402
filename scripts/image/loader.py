from pathlib import Path

from PIL import Image

from scripts.utils.logger import logger


class ImageLoader:

    def __init__(self, image_path: Path):

        self.image_path = Path(image_path)

    def load(self) -> Image.Image:

        if not self.image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {self.image_path}"
            )

        logger.info(f"Loading image: {self.image_path.name}")
        image = Image.open(self.image_path)

        logger.info(f"Image Size : {image.width}x{image.height}")
        logger.info(f"Image Mode : {image.mode}")

        return image