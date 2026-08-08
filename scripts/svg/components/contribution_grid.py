from scripts.svg.components.base import SVGComponent

from scripts.svg.elements import SVGRect

from scripts.svg.theme import DEFAULT_THEME

from scripts.animation.smil import AnimateOpacity
from scripts.animation.easing import Easings


class ContributionGridComponent(SVGComponent):
    """
    Renders the GitHub contribution grid.

    Responsibilities:

    - contribution colors
    - cell geometry
    - cell styling
    - cell-level animation

    The generator controls the high-level
    week timing.
    """

    # ============================================================
    # Contribution Colors
    # ============================================================

    COLORS = {
        0: "#21262D",
        1: "#0E4429",
        2: "#006D32",
        3: "#26A641",
        4: "#39D353",
    }

    # ============================================================
    # Animation Configuration
    # ============================================================

    # How long one cell takes to appear.
    CELL_DURATION = 0.10

    # Delay between cells inside the same week.
    #
    # This is deliberately visible but still fast.
    CELL_STAGGER = 0.008

    # Small pause after a week finishes before
    # the next week starts.
    WEEK_GAP = 0.01

    # ============================================================
    # Initialization
    # ============================================================

    def __init__(
        self,
        cells,
        theme=None,
    ):

        super().__init__()

        self.cells = cells

        self.theme = (
            theme
            or DEFAULT_THEME
        )

        self._week_begin = None

    # ============================================================
    # Animation Schedule
    # ============================================================

    def set_animation_schedule(
        self,
        week_begin,
    ):
        """
        Supplies the high-level week timing.

        week_begin must be a callable:

            week_begin(week_index)

        returning a time such as:

            "0.000s"
            "0.198s"
            "0.396s"
        """

        self._week_begin = (
            week_begin
        )

        return self

    # ============================================================
    # Cell Timing
    # ============================================================

    def _cell_begin(
        self,
        cell,
    ):
        """
        Calculates the final animation start
        time for a contribution cell.

        Timing:

            week start
                +
            day offset
        """

        # --------------------------------------------------------
        # Week start
        # --------------------------------------------------------

        if self._week_begin is not None:

            week_begin = self._week_begin(
                cell.week
            )

            try:

                week_seconds = float(
                    str(
                        week_begin
                    ).replace(
                        "s",
                        "",
                    )
                )

            except (
                TypeError,
                ValueError,
            ):

                week_seconds = 0.0

        else:

            week_seconds = 0.0

        # --------------------------------------------------------
        # Position inside week
        # --------------------------------------------------------

        cell_offset = (
            cell.day
            * self.CELL_STAGGER
        )

        # --------------------------------------------------------
        # Final begin time
        # --------------------------------------------------------

        begin = (
            week_seconds
            + cell_offset
        )

        return (
            f"{begin:.3f}s"
        )

    # ============================================================
    # Render
    # ============================================================

    def render(self):

        elements = []

        # ========================================================
        # Contribution Cells
        # ========================================================

        for cell in self.cells:

            # ----------------------------------------------------
            # Contribution level
            # ----------------------------------------------------

            level = max(
                0,
                min(
                    4,
                    int(
                        cell.contribution.level
                    ),
                ),
            )

            # ----------------------------------------------------
            # Resolve color
            # ----------------------------------------------------

            fill = self.COLORS.get(
                level,
                self.COLORS[0],
            )

            # ----------------------------------------------------
            # Create cell
            # ----------------------------------------------------

            element = SVGRect(

                x=cell.x,

                y=cell.y,

                width=cell.size,

                height=cell.size,

                fill=fill,

                stroke=self.theme.border,

                stroke_width=0.5,

                rx=2,

                ry=2,

            )

            # ----------------------------------------------------
            # Start invisible
            # ----------------------------------------------------

            element.set_opacity(0)

            # ----------------------------------------------------
            # Cell reveal
            # ----------------------------------------------------

            element.animate(

                AnimateOpacity(

                    begin=self._cell_begin(
                        cell
                    ),

                    duration=(
                        f"{self.CELL_DURATION:.3f}s"
                    ),

                    easing=Easings.EASE_OUT,

                )

            )

            elements.append(
                element
            )

        return elements