from config.settings import GENERATED_SVG

from scripts.generators.base import BaseGenerator
from scripts.github.statistics import GitHubStatisticsEngine

from scripts.svg.document import SVGDocument
from scripts.svg.theme import DEFAULT_THEME

from scripts.svg.components.container import ContainerComponent
from scripts.svg.components.heading import HeadingComponent
from scripts.svg.components.footer import FooterComponent
from scripts.svg.components.language_bar import LanguageBarComponent

from scripts.svg.layouts.language_layout import LanguageLayout

from scripts.utils.logger import logger


class LanguagesGenerator(BaseGenerator):
    """
    Generates languages.svg.

    Responsibilities:

    - Load GitHub language data
    - Build the language layout
    - Create language components
    - Control the animation timing of each row

    Individual language bars are responsible for
    how they animate.

    This generator is responsible only for
    when they animate.
    """

    # ============================================================
    # Animation Configuration
    # ============================================================

    LANGUAGE_STAGGER = 0.12

    # ============================================================
    # Initialization
    # ============================================================

    def __init__(self):

        super().__init__()

        self.statistics = (
            GitHubStatisticsEngine()
        )

        self.layout = LanguageLayout()

    # ============================================================
    # Generate
    # ============================================================

    def generate(self):

        logger.info("=" * 60)

        logger.info(
            "LANGUAGES GENERATOR"
        )

        logger.info("=" * 60)

        # --------------------------------------------------------
        # Load GitHub data
        # --------------------------------------------------------

        profile = self.load_profile(
            repositories=True,
        )

        # --------------------------------------------------------
        # Calculate language statistics
        # --------------------------------------------------------

        self.statistics.language_statistics(
            profile,
        )

        # --------------------------------------------------------
        # Render
        # --------------------------------------------------------

        self.render_svg(
            profile,
        )

    # ============================================================
    # Animation Timing
    # ============================================================

    def _language_animation_begin(
        self,
        index,
    ):
        """
        Calculates the start time for a language row.

        The timing is owned by the generator so the
        component itself remains reusable.

        Example:

            language 1 -> 0.00s
            language 2 -> 0.12s
            language 3 -> 0.24s
            language 4 -> 0.36s
        """

        begin = (
            index
            * self.LANGUAGE_STAGGER
        )

        return (
            f"{begin:.3f}s"
        )

    # ============================================================
    # Render SVG
    # ============================================================

    def render_svg(
        self,
        profile,
    ):

        logger.info(
            "Rendering languages.svg"
        )

        # --------------------------------------------------------
        # Build responsive layout
        # --------------------------------------------------------

        layout = self.layout.build(
            profile,
        )

        # --------------------------------------------------------
        # SVG document
        # --------------------------------------------------------

        document = SVGDocument(

            width=layout.width,

            height=layout.height,

            background=(
                DEFAULT_THEME.page_background
            ),

        )

        # ========================================================
        # Container
        # ========================================================

        document.add(

            ContainerComponent(

                x=layout.container.x,

                y=layout.container.y,

                width=layout.container.width,

                height=layout.container.height,

            )

        )

        # ========================================================
        # Heading
        # ========================================================

        document.add(

            HeadingComponent(

                title="Programming Languages",

                subtitle=(
                    "Repository language distribution"
                ),

                x=layout.heading.x,

                y=layout.heading.y,

            )

        )

        # ========================================================
        # Language Bars
        # ========================================================

        for index, language in enumerate(
            layout.cards
        ):

            animation_begin = (
                self._language_animation_begin(
                    index
                )
            )

            document.add(

                LanguageBarComponent(

                    language=language.name,

                    percentage=language.percentage,

                    x=language.x,

                    y=language.y,

                    width=language.width,

                    height=language.height,

                    animation_begin=animation_begin,

                )

            )

        # ========================================================
        # Footer
        # ========================================================

        document.add(

            FooterComponent(

                text=(
                    "Generated automatically "
                    "using Profile Generator"
                ),

                x=layout.footer.x,

                y=layout.footer.y,

            )

        )

        # ========================================================
        # Save
        # ========================================================

        document.save(

            GENERATED_SVG
            / "languages.svg"

        )

        logger.info(
            "languages.svg generated."
        )