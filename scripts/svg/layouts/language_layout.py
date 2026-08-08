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
# Language Bar
# ============================================================

@dataclass
class LanguageBarPosition:

    name: str
    percentage: float

    x: float
    y: float

    width: float
    height: float


# ============================================================
# Document Layout
# ============================================================

@dataclass
class LanguageDocumentLayout:

    width: float
    height: float

    container: Rectangle

    heading: Point

    footer: Point

    cards: list[LanguageBarPosition]


# ============================================================
# Layout Engine
# ============================================================

class LanguageLayout:
    """
    Calculates the complete layout
    for languages.svg.
    """

    def __init__(
        self,
        padding=24,
        container_padding=24,
        row_gap=52,
        bar_height=14,
    ):

        self.padding = padding
        self.container_padding = container_padding

        self.row_gap = row_gap
        self.bar_height = bar_height

    # --------------------------------------------------------

    def build(
        self,
        profile: GitHubProfile,
    ) -> LanguageDocumentLayout:

        container_width = 860

        bar_width = (
            container_width
            - self.container_padding * 2
        )

        start_x = (
            self.padding
            + self.container_padding
        )

        start_y = 108

        cards = []

        for index, language in enumerate(profile.languages):

            cards.append(

                LanguageBarPosition(

                    name=language.name,

                    percentage=round(
                        language.percentage,
                        2,
                    ),

                    x=start_x,

                    y=start_y
                    + index * self.row_gap,

                    width=bar_width,

                    height=self.bar_height,

                )

            )

        bars_height = len(cards) * self.row_gap

        container_height = (
            90
            + bars_height
            + 60
        )

        document_width = (
            container_width
            + self.padding * 2
        )

        document_height = (
            container_height
            + self.padding * 2
        )

        return LanguageDocumentLayout(

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

            cards=cards,

        )