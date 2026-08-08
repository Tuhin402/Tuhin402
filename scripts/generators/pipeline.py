from scripts.utils.logger import logger


class GeneratorPipeline:
    """
    Executes all registered generators
    in sequence.
    """

    def __init__(self):

        self.generators = []

    # --------------------------------------------------

    def register(self, generator,):

        self.generators.append(generator)
        return self

    # --------------------------------------------------

    def run(self):

        logger.info("=" * 60)
        logger.info("GENERATOR PIPELINE")
        logger.info("=" * 60)

        for generator in self.generators:

            logger.info(f"Running {generator.__class__.__name__}")
            generator.generate()

        logger.info("Pipeline Complete.")