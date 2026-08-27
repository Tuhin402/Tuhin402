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
    - optional display sizing

    The internal SVG geometry remains controlled
    by width, height and viewBox.

    display_width is optional and affects only
    the intrinsic rendered size of the SVG.
    """

    def __init__(
        self,
        width,
        height,
        background="none",
        responsive=True,
        display_width=None,
    ):

        self.width = width
        self.height = height

        self.background = background
        self.responsive = responsive

        # ------------------------------------------------
        # Optional display dimensions
        # ------------------------------------------------

        self.display_width = display_width

        self.display_height = None

        if display_width is not None:

            if width > 0:

                self.display_height = (
                    display_width
                    * height
                    / width
                )

        # ------------------------------------------------
        # ViewBox
        # ------------------------------------------------

        self.viewbox = (
            SVGViewBoxEngine()
            .build(
                width,
                height,
            )
        )

        self.styles = []

        self.add_default_motion_styles()

        self.definitions = []

        self.elements = []

    # ------------------------------------------------

    def add_style(
        self,
        style,
    ):

        self.styles.append(
            style
        )

    # ------------------------------------------------

    def add_default_motion_styles(self):
        """Add reusable local-browser motion and hover styles."""

        self.styles.append(
            """
<style>

@keyframes pgPulse {
    0%, 100% { opacity: 0.82; }
    50% { opacity: 1; }
}

@keyframes pgCardGlow {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.035); }
}

.pg-container {
    transform-box: fill-box;
    transform-origin: center;
    transition: filter 220ms ease, transform 220ms ease;
}

.pg-container:hover {
    filter: brightness(1.06);
}

.pg-stat-card {
    transform-box: fill-box;
    transform-origin: center;
    animation: pgCardGlow 5s ease-in-out infinite;
    transition: transform 220ms ease;
}

.pg-stat-card:hover {
    transform: translateY(-3px);
}

.pg-language-progress {
    animation: pgPulse 3.2s ease-in-out infinite;
    transform-box: fill-box;
    transform-origin: left center;
    transition: filter 220ms ease;
}

.pg-language-progress:hover {
    filter: brightness(1.16);
}

.pg-grid-cell {
    transform-box: fill-box;
    transform-origin: center;
    transition: transform 140ms ease, filter 140ms ease;
}

.pg-grid-cell:hover {
    transform: scale(1.24);
    filter: brightness(1.15);
}

.pg-grid-cell-hot {
    animation: pgPulse 2.6s ease-in-out infinite;
}

</style>
"""
        )
        return self

    # ------------------------------------------------

    def add_definition(
        self,
        definition,
    ):

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

        self.definitions.append(
            definition
        )

    # ------------------------------------------------

    def add(
        self,
        element: SVGElement,
    ):

        self.elements.append(
            element
        )

    # ------------------------------------------------

    def _render_dimensions(self):
        """
        Determines the SVG's external display
        dimensions.

        If display_width is not provided,
        the existing responsive behavior is
        preserved exactly.
        """

        # ------------------------------------------------
        # Custom display size
        # ------------------------------------------------

        if self.display_width is not None:

            width = str(
                self.display_width
            )

            height = str(
                self.display_height
            )

            return width, height

        # ------------------------------------------------
        # Existing responsive behavior
        # ------------------------------------------------

        if self.responsive:

            return "100%", "100%"

        return (
            str(self.width),
            str(self.height),
        )

    # ------------------------------------------------

    def render(self):

        logger.info(
            "Rendering SVG Document"
        )

        svg = []

        svg.append(
            '<?xml version="1.0" encoding="UTF-8"?>'
        )

        # ------------------------------------------------
        # Display dimensions
        # ------------------------------------------------

        width, height = (
            self._render_dimensions()
        )

        svg.append(

            f'<svg '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'width="{width}" '
            f'height="{height}" '
            f'viewBox="{self.viewbox.value}" '
            f'preserveAspectRatio='
            f'"{self.viewbox.preserve_aspect_ratio}">'

        )

        # ------------------------------------------------
        # Background
        # ------------------------------------------------

        if self.background not in (
            None,
            "",
            "none",
            "transparent",
        ):

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

            svg.append(
                style
            )

        # ------------------------------------------------
        # Definitions
        # ------------------------------------------------

        if self.definitions:

            svg.append(
                "<defs>"
            )

            for definition in (
                self.definitions
            ):

                svg.append(
                    definition.render()
                )

            svg.append(
                "</defs>"
            )

        # ------------------------------------------------
        # Components
        # ------------------------------------------------

        for component in self.elements:

            rendered = (
                component.render()
            )

            # -----------------------------
            # list
            # -----------------------------

            if isinstance(
                rendered,
                list,
            ):

                for element in rendered:

                    if isinstance(
                        element,
                        str,
                    ):

                        svg.append(
                            element
                        )

                    else:

                        svg.append(
                            element.render()
                        )

            # -----------------------------
            # raw string
            # -----------------------------

            elif isinstance(
                rendered,
                str,
            ):

                svg.append(
                    rendered
                )

            # -----------------------------
            # SVGElement
            # -----------------------------

            else:

                svg.append(
                    rendered.render()
                )

        svg.append(
            "</svg>"
        )

        return "\n".join(svg)

    # ------------------------------------------------

    def save(
        self,
        output,
    ):

        output = Path(
            output
        )

        output.write_text(

            self.render(),

            encoding="utf8",

        )

        logger.info(
            f"SVG Saved : {output.name}"
        )