from config.settings import GENERATED_SVG

from scripts.generators.base import BaseGenerator
from scripts.github.statistics import GitHubStatisticsEngine

from scripts.svg.document import SVGDocument
from scripts.svg.theme import DEFAULT_THEME

from scripts.svg.components.container import ContainerComponent
from scripts.svg.components.heading import HeadingComponent
from scripts.svg.components.footer import FooterComponent
from scripts.svg.components.statistic_card import StatisticCardComponent

from scripts.svg.layouts.streak_layout import StreakLayout

from scripts.utils.logger import logger


class StreakGenerator(BaseGenerator):
    """
    Generates streak.svg.

    Responsibilities:

    - Load GitHub contribution data
    - Calculate streak statistics
    - Build the responsive streak layout
    - Create reusable SVG components
    - Control animation timing

    Visual styling and individual card animation
    remain inside the reusable components.
    """

    # ============================================================
    # Animation Configuration
    # ============================================================

    CARD_STAGGER = 0.16

    # ============================================================
    # Initialization
    # ============================================================

    def __init__(self):

        super().__init__()

        self.statistics = (
            GitHubStatisticsEngine()
        )

        self.layout = StreakLayout()

        self.theme = DEFAULT_THEME

    # ============================================================
    # Generate
    # ============================================================

    def generate(self):

        logger.info("=" * 60)

        logger.info(
            "STREAK GENERATOR"
        )

        logger.info("=" * 60)

        # --------------------------------------------------------
        # Load GitHub contribution data
        # --------------------------------------------------------

        profile = self.load_profile(
            repositories=True,
            contributions=True,
        )

        # --------------------------------------------------------
        # Calculate statistics
        # --------------------------------------------------------

        stats = self.statistics.compute(
            profile
        )

        # --------------------------------------------------------
        # Render
        # --------------------------------------------------------

        self.render_svg(
            profile,
            stats,
        )

    # ============================================================
    # Card Animation Timing
    # ============================================================

    def _card_animation_begin(
        self,
        index,
    ):
        """
        Calculates the animation start time
        for each streak card.

        Card 1:
            0.00s

        Card 2:
            0.16s
        """

        begin = (
            index
            * self.CARD_STAGGER
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
        stats,
    ):

        logger.info(
            "Rendering streak.svg"
        )

        # --------------------------------------------------------
        # Build responsive layout
        # --------------------------------------------------------

        layout = self.layout.build(
            stats
        )

        # --------------------------------------------------------
        # SVG document
        # --------------------------------------------------------

        document = SVGDocument(

            width=layout.width,

            height=layout.height,

            background=(
                self.theme.page_background
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

                title=(
                    f"{profile.username}"
                    "'s Contribution Streak"
                ),

                subtitle=(
                    "Current and longest "
                    "contribution streak"
                ),

                x=layout.heading.x,

                y=layout.heading.y,

            )

        )

        # ========================================================
        # Streak Cards
        # ========================================================

        for index, card in enumerate(
            layout.cards
        ):

            animation_begin = (
                self._card_animation_begin(
                    index
                )
            )

            document.add(

                StatisticCardComponent(

                    title=card.title,

                    value=card.value,

                    x=card.x,

                    y=card.y,

                    width=card.width,

                    height=card.height,

                    animation_begin=(
                        animation_begin
                    ),

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
            / "streak.svg"

        )

        logger.info(
            "streak.svg generated."
        )