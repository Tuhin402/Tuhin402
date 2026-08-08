from dataclasses import dataclass

from scripts.github.models import GitHubProfile


# ============================================================
# Geometry
# ============================================================

@dataclass
class Point:
    x: float
    y: float


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float


# ============================================================
# Contribution Cell
# ============================================================

@dataclass
class ContributionCellPosition:

    contribution: object

    x: float
    y: float

    size: float

    # --------------------------------------------------------
    # Animation metadata
    # --------------------------------------------------------

    week: int
    day: int


# ============================================================
# Whole Document Layout
# ============================================================

@dataclass
class YearDocumentLayout:

    width: float
    height: float

    container: Rectangle

    heading: Point

    footer: Point

    cells: list[ContributionCellPosition]

    # --------------------------------------------------------
    # Grid metadata
    # --------------------------------------------------------

    weeks: int


# ============================================================
# Layout Engine
# ============================================================

class YearLayout:
    """
    Calculates the complete responsive layout
    of year.svg.

    The layout owns geometry only.

    It also exposes week/day metadata so the
    generator can create deterministic animation
    timing without having to recalculate the
    contribution grid geometry.
    """

    def __init__(
        self,
        padding=24,
        container_padding=24,
        cell_size=12,
        gap=4,
    ):

        self.padding = padding
        self.container_padding = container_padding

        self.cell_size = cell_size
        self.gap = gap

    # ============================================================
    # Build
    # ============================================================

    def build(
        self,
        profile: GitHubProfile,
    ) -> YearDocumentLayout:

        # --------------------------------------------------------
        # Grid origin
        # --------------------------------------------------------

        start_x = (
            self.padding
            + self.container_padding
        )

        start_y = 100

        # --------------------------------------------------------
        # Contribution data
        # --------------------------------------------------------

        contributions = (
            profile.contributions
        )

        # --------------------------------------------------------
        # Calculate week count
        # --------------------------------------------------------

        weeks = (
            len(contributions)
            + 6
        ) // 7

        # --------------------------------------------------------
        # Cell positions
        # --------------------------------------------------------

        cells = []

        for index, contribution in enumerate(
            contributions
        ):

            week = (
                index // 7
            )

            day = (
                index % 7
            )

            x = (
                start_x
                + week
                * (
                    self.cell_size
                    + self.gap
                )
            )

            y = (
                start_y
                + day
                * (
                    self.cell_size
                    + self.gap
                )
            )

            cells.append(

                ContributionCellPosition(

                    contribution=contribution,

                    x=x,
                    y=y,

                    size=self.cell_size,

                    week=week,
                    day=day,

                )

            )

        # ========================================================
        # Grid dimensions
        # ========================================================

        if weeks > 0:

            grid_width = (
                (
                    weeks
                    * self.cell_size
                )
                +
                (
                    max(
                        0,
                        weeks - 1,
                    )
                    * self.gap
                )
            )

        else:

            grid_width = 0

        grid_height = (
            (
                7
                * self.cell_size
            )
            +
            (
                6
                * self.gap
            )
        )

        # ========================================================
        # Container
        # ========================================================

        container_width = max(

            860,

            grid_width
            + (
                self.container_padding
                * 2
            ),

        )

        container_height = (

            100

            +

            grid_height

            +

            60

        )

        # ========================================================
        # Document
        # ========================================================

        document_width = (

            container_width
            + (
                self.padding
                * 2
            )

        )

        document_height = (

            container_height
            + (
                self.padding
                * 2
            )

        )

        # ========================================================
        # Return layout
        # ========================================================

        return YearDocumentLayout(

            width=document_width,

            height=document_height,

            container=Rectangle(

                x=self.padding,

                y=self.padding,

                width=container_width,

                height=container_height,

            ),

            heading=Point(

                x=start_x,

                y=56,

            ),

            footer=Point(

                x=start_x,

                y=document_height - 32,

            ),

            cells=cells,

            weeks=weeks,

        )