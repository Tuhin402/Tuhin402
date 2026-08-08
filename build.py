from scripts.generators.pipeline import GeneratorPipeline

from scripts.generators.profile_generator import ProfileGenerator
from scripts.generators.stats_generator import StatsGenerator
from scripts.generators.languages_generator import LanguagesGenerator
from scripts.generators.year_generator import YearGenerator
from scripts.generators.streak_generator import StreakGenerator
from scripts.generators.readme_generator import ReadmeGenerator

from scripts.utils.filesystem import ensure_directories
from scripts.utils.logger import logger


def main():

    logger.info("=" * 60)
    logger.info("PROFILE GENERATOR")
    logger.info("=" * 60)

    ensure_directories()
    (
        GeneratorPipeline()
        .register(ProfileGenerator())
        .register(StatsGenerator())
        .register(LanguagesGenerator())
        .register(YearGenerator())
        .register(StreakGenerator())
        .register(ReadmeGenerator())
        .run()
    )


if __name__ == "__main__":

    main()