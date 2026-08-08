from dataclasses import dataclass

from scripts.github.models import GitHubStatistics


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
# Streak Card
# ============================================================

@dataclass
class StreakCardPosition:

    title: str
    value: str

    x: float
    y: float

    width: float
    height: float


# ============================================================
# Whole Document
# ============================================================

@dataclass
class StreakDocumentLayout:

    width: float
    height: float

    container: Rectangle

    heading: Point

    footer: Point

    cards: list[StreakCardPosition]


# ============================================================
# Layout Engine
# ============================================================

class StreakLayout:
    """
    Calculates the complete responsive layout
    for streak.svg.

    The layout follows the same geometry model
    used by stats.svg and languages.svg.
    """

    def __init__(
        self,
        padding=24,
        container_padding=24,
        card_width=300,
        card_height=150,
        gap=40,
    ):

        self.padding = padding

        self.container_padding = (
            container_padding
        )

        self.card_width = card_width
        self.card_height = card_height

        self.gap = gap

    # ========================================================
    # Build
    # ========================================================

    def build(
        self,
        statistics: GitHubStatistics,
    ) -> StreakDocumentLayout:
        """
        Calculates the complete streak layout.
        """

        # ----------------------------------------------------
        # Card geometry
        # ----------------------------------------------------

        cards_width = (
            self.card_width * 2
            + self.gap
        )

        # ----------------------------------------------------
        # Container geometry
        # ----------------------------------------------------

        container_width = (
            cards_width
            + self.container_padding * 2
        )

        # ----------------------------------------------------
        # Document width
        # ----------------------------------------------------

        document_width = (
            container_width
            + self.padding * 2
        )

        # ----------------------------------------------------
        # Card origin
        # ----------------------------------------------------

        cards_start_x = (
            self.padding
            + self.container_padding
        )

        cards_start_y = 120

        # ----------------------------------------------------
        # Cards
        # ----------------------------------------------------

        cards = [

            StreakCardPosition(

                title="Current Streak",

                value=str(
                    statistics.current_streak
                ),

                x=cards_start_x,

                y=cards_start_y,

                width=self.card_width,

                height=self.card_height,

            ),

            StreakCardPosition(

                title="Longest Streak",

                value=str(
                    statistics.longest_streak
                ),

                x=(
                    cards_start_x
                    + self.card_width
                    + self.gap
                ),

                y=cards_start_y,

                width=self.card_width,

                height=self.card_height,

            ),

        ]

        # ----------------------------------------------------
        # Container height
        # ----------------------------------------------------

        container_height = (
            90
            + self.card_height
            + 70
        )

        # ----------------------------------------------------
        # Document height
        # ----------------------------------------------------

        document_height = (
            container_height
            + self.padding * 2
        )

        # ----------------------------------------------------
        # Final layout
        # ----------------------------------------------------

        return StreakDocumentLayout(

            width=document_width,

            height=document_height,

            container=Rectangle(

                x=self.padding,

                y=self.padding,

                width=container_width,

                height=container_height,

            ),

            heading=Point(

                x=(
                    self.padding
                    + self.container_padding
                ),

                y=56,

            ),

            footer=Point(

                x=(
                    self.padding
                    + self.container_padding
                ),

                y=(
                    document_height
                    - 32
                ),

            ),

            cards=cards,

        )