from pathlib import Path

from scripts.svg.elements import SVGElement
from scripts.svg.viewbox import SVGViewBoxEngine

from scripts.utils.logger import logger


class SVGDocument:
    """
    Represents a complete SVG document.

    Supports:

    - styles
    - reusable <defs>
    - SVG elements
    """

    def __init__(
        self,
        width,
        height,
        background="none",
        responsive=True,
    ):

        self.width = width
        self.height = height

        self.background = background
        self.responsive = responsive

        self.viewbox = (
            SVGViewBoxEngine()
            .build(width, height)
        )

        self.styles = []

        # NEW
        self.definitions = []

        self.elements = []

    # ------------------------------------------------

    def add_style(self, style):

        self.styles.append(style)

    # ------------------------------------------------
    # NEW
    # ------------------------------------------------

    def add_definition(self, definition):

        """
        Adds anything that belongs
        inside the SVG <defs> block.

        Examples:

        - mask
        - clipPath
        - linearGradient
        - radialGradient
        - filter
        """

        self.definitions.append(definition)

    # ------------------------------------------------

    def add(self, element: SVGElement):

        self.elements.append(element)

    # ------------------------------------------------

    def render(self):

        logger.info("Rendering SVG Document")

        svg = []

        svg.append(
            '<?xml version="1.0" encoding="UTF-8"?>'
        )

        if self.responsive:

            width = "100%"
            height = "100%"

        else:

            width = str(self.width)
            height = str(self.height)

        svg.append(

            f'<svg '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" '
            f'height="{height}" '
            f'viewBox="{self.viewbox.value}" '
            f'preserveAspectRatio="{self.viewbox.preserve_aspect_ratio}">'
        )

        # ------------------------------------------------
        # Background
        # ------------------------------------------------

        if self.background not in (None, "", "none", "transparent"):

            svg.append(

                f'<rect '
                f'width="100%" '
                f'height="100%" '
                f'fill="{self.background}" />'

            )

        # ------------------------------------------------
        # Styles
        # ------------------------------------------------

        for style in self.styles:

            svg.append(style)

        # ------------------------------------------------
        # Definitions
        # ------------------------------------------------

        if self.definitions:

            svg.append("<defs>")

            for definition in self.definitions:

                svg.append(
                    definition.render()
                )

            svg.append("</defs>")

        # ------------------------------------------------
        # Components
        # ------------------------------------------------

        for component in self.elements:

            rendered = component.render()

            # -----------------------------
            # list
            # -----------------------------

            if isinstance(rendered, list):

                for element in rendered:

                    if isinstance(element, str):

                        svg.append(element)

                    else:

                        svg.append(
                            element.render()
                        )

            # -----------------------------
            # raw string
            # -----------------------------

            elif isinstance(rendered, str):

                svg.append(rendered)

            # -----------------------------
            # SVGElement
            # -----------------------------

            else:

                svg.append(
                    rendered.render()
                )

        svg.append("</svg>")

        return "\n".join(svg)

    # ------------------------------------------------

    def save(self, output):

        output = Path(output)

        output.write_text(

            self.render(),

            encoding="utf8",

        )

        logger.info(
            f"SVG Saved : {output.name}"
        )