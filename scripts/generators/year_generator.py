from config.settings import GENERATED_SVG

from scripts.generators.base import BaseGenerator

from scripts.svg.document import SVGDocument
from scripts.svg.theme import DEFAULT_THEME

from scripts.svg.components.container import ContainerComponent
from scripts.svg.components.heading import HeadingComponent
from scripts.svg.components.footer import FooterComponent
from scripts.svg.components.contribution_grid import (
    ContributionGridComponent,
)

from scripts.svg.layouts.year_layout import YearLayout

from scripts.utils.logger import logger


class YearGenerator(BaseGenerator):
    """
    Generates year.svg.

    Responsibilities:

    - Load GitHub contribution data
    - Build the responsive year layout
    - Control high-level animation timing
    - Compose reusable SVG components

    Individual contribution cell rendering remains
    inside ContributionGridComponent.
    """

    # ============================================================
    # Animation Configuration
    # ============================================================

    # Must match the contribution grid timing.

    CELL_DURATION = (
        ContributionGridComponent.CELL_DURATION
    )

    CELL_STAGGER = (
        ContributionGridComponent.CELL_STAGGER
    )

    WEEK_GAP = (
        ContributionGridComponent.WEEK_GAP
    )

    # ============================================================
    # Initialization
    # ============================================================

    def __init__(self):

        super().__init__()

        self.layout = YearLayout()

        self.theme = DEFAULT_THEME

    # ============================================================
    # Generate
    # ============================================================

    def generate(self):

        logger.info("=" * 60)

        logger.info(
            "YEAR GENERATOR"
        )

        logger.info("=" * 60)

        # --------------------------------------------------------
        # Load contribution data
        # --------------------------------------------------------

        profile = self.load_profile(
            contributions=True,
        )

        # --------------------------------------------------------
        # Render
        # --------------------------------------------------------

        self.render_svg(
            profile
        )

    # ============================================================
    # Week Animation Timing
    # ============================================================

    def _week_duration(self):
        """
        Calculates the amount of time required
        for a complete seven-day week reveal.

        The final cell is day 6, therefore:

            6 * CELL_STAGGER
                +
            CELL_DURATION

        Then we add a tiny visual gap before
        the next week begins.
        """

        final_cell_offset = (
            6
            * self.CELL_STAGGER
        )

        return (
            final_cell_offset
            + self.CELL_DURATION
            + self.WEEK_GAP
        )

    # ------------------------------------------------------------

    def _week_animation_begin(
        self,
        week,
    ):
        """
        Returns the exact start time for a week.

        Every week begins only after the previous
        week's complete reveal has finished.

        Example with the current configuration:

            Week 0 -> 0.000s
            Week 1 -> 0.288s
            Week 2 -> 0.576s
            Week 3 -> 0.864s
            ...
        """

        begin = (
            week
            * self._week_duration()
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
            "Rendering year.svg"
        )

        # --------------------------------------------------------
        # Build layout
        # --------------------------------------------------------

        layout = self.layout.build(
            profile
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

                title="Contribution Calendar",

                subtitle=(
                    "GitHub activity "
                    "over the last year"
                ),

                x=layout.heading.x,

                y=layout.heading.y,

            )

        )

        # ========================================================
        # Contribution Grid
        # ========================================================

        grid = ContributionGridComponent(

            cells=layout.cells,

            theme=self.theme,

        )

        # --------------------------------------------------------
        # IMPORTANT
        #
        # The generator now actually connects the week-level
        # timeline to the contribution grid.
        # --------------------------------------------------------

        grid.set_animation_schedule(

            week_begin=(
                self._week_animation_begin
            ),

        )

        document.add(
            grid
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
        # Animation information
        # ========================================================

        if layout.weeks > 0:

            total_duration = (
                (
                    layout.weeks - 1
                )
                * self._week_duration()
                + self.CELL_DURATION
                + (
                    6
                    * self.CELL_STAGGER
                )
            )

            logger.info(
                "Year Grid Weeks : "
                f"{layout.weeks}"
            )

            logger.info(
                "Year Grid Animation Duration : "
                f"{total_duration:.3f}s"
            )

        # ========================================================
        # Save
        # ========================================================

        document.save(

            GENERATED_SVG
            / "year.svg"

        )

        logger.info(
            "year.svg generated."
        )