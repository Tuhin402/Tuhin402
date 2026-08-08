from dataclasses import dataclass

from scripts.github.models import GitHubStatistics


# ============================================================
# Basic Geometry
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
# Statistic Card
# ============================================================

@dataclass
class StatisticCardPosition:

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
class StatsDocumentLayout:

    width: float
    height: float

    container: Rectangle
    heading: Point
    footer: Point

    cards: list[StatisticCardPosition]


# ============================================================
# Layout Engine
# ============================================================

class StatsLayout:
    """
    Calculates the complete responsive
    layout of stats.svg.
    """

    def __init__(
        self,
        padding=24,
        container_padding=24,
        card_width=180,
        card_height=90,
        gap=20,
        columns=4,
    ):

        self.padding = padding
        self.container_padding = container_padding

        self.card_width = card_width
        self.card_height = card_height

        self.gap = gap
        self.columns = columns

    # ---------------------------------------------------------

    def build(
        self,
        stats: GitHubStatistics,
    ) -> StatsDocumentLayout:

        metrics = [

            ("Repositories", stats.total_repositories),
            ("Stars", stats.total_stars),
            ("Forks", stats.total_forks),
            ("Followers", stats.total_followers),

            ("Following", stats.total_following),
            ("Contributions", stats.total_contributions),
            ("Longest Streak", stats.longest_streak),
            ("Top Language", stats.top_language),

        ]

        rows = (
            len(metrics)
            + self.columns
            - 1
        ) // self.columns

        # -----------------------------------------------------
        # Card origin
        # -----------------------------------------------------

        cards_start_x = (
            self.padding
            + self.container_padding
        )

        cards_start_y = 120

        cards = []

        for index, (title, value) in enumerate(metrics):

            row = index // self.columns
            column = index % self.columns

            x = (
                cards_start_x
                + column * (self.card_width + self.gap)
            )

            y = (
                cards_start_y
                + row * (self.card_height + self.gap)
            )

            cards.append(

                StatisticCardPosition(

                    title=title,
                    value=str(value),

                    x=x,
                    y=y,

                    width=self.card_width,
                    height=self.card_height,

                )

            )

        # -----------------------------------------------------
        # Calculate exact content width
        # -----------------------------------------------------

        cards_width = (

            self.columns * self.card_width

            +

            (self.columns - 1) * self.gap

        )

        container_width = (

            cards_width

            +

            self.container_padding * 2

        )

        document_width = (

            container_width

            +

            self.padding * 2

        )

        # -----------------------------------------------------
        # Heights
        # -----------------------------------------------------

        cards_height = (

            rows * self.card_height

            +

            (rows - 1) * self.gap

        )

        container_height = (

            90              # heading

            +

            cards_height

            +

            70              # footer

        )

        document_height = (

            container_height

            +

            self.padding * 2

        )

        # -----------------------------------------------------

        return StatsDocumentLayout(

            width=document_width,
            height=document_height,

            container=Rectangle(

                x=self.padding,
                y=self.padding,

                width=container_width,
                height=container_height,

            ),

            heading=Point(

                x=self.padding + self.container_padding,
                y=56,

            ),

            footer=Point(

                x=self.padding + self.container_padding,
                y=document_height - 32,

            ),

            cards=cards,

        )