from config.settings import (
    GENERATED_SVG,
    JETBRAINS_MONO,
    ASCII_DISPLAY_WIDTH,
)

from scripts.svg.document import SVGDocument
from scripts.svg.elements import SVGTextBlock
from scripts.svg.font_engine import SVGFontEngine
from scripts.svg.layout import SVGLayout
from scripts.svg.typography import Typography

from scripts.svg.masks import SVGMaskReveal

from scripts.utils.logger import logger


class SVGRenderer:
    """
    Converts an ASCII matrix into a self-contained SVG.

    The portrait is rendered one line at a time.

    Each line receives its own animated mask which
    reveals the ASCII characters from left to right.

    Every line starts only after the previous line
    has completely finished.

    Animation duration is calculated dynamically from
    the number of visible ASCII characters in that row.
    """

    def __init__(self):

        self.typography = Typography()

        self.layout = SVGLayout(
            self.typography
        )

        self.font = SVGFontEngine(
            JETBRAINS_MONO
        )

    # ============================================================
    # Dynamic row duration
    # ============================================================

    def _row_duration(
        self,
        character_count,
    ):
        """
        Calculates a fast, dynamic reveal duration.

        Longer rows still take longer than shorter rows.

        The calculated duration is compressed so that the
        complete portrait remains around 15 seconds for
        the current ASCII portrait while preserving the
        dynamic relationship between row lengths.
        """

        seconds_per_character = 0.004

        minimum_duration = 0.05
        maximum_duration = 0.35

        duration = (
            character_count
            * seconds_per_character
        )

        duration = max(
            minimum_duration,
            duration,
        )

        duration = min(
            maximum_duration,
            duration,
        )

        # --------------------------------------------------------
        # Compress the complete animation timeline.
        #
        # Current observed total:
        # approximately 35 seconds.
        #
        # Desired total:
        # approximately 15 seconds.
        #
        # 15 / 35 = 0.428571
        # --------------------------------------------------------

        duration *= 0.428571

        return duration

    # ============================================================
    # Sequential row timing
    # ============================================================

    def _row_begin(
        self,
        current_time,
    ):
        """
        Returns the start time for the current row.

        current_time is maintained by the renderer,
        therefore every row begins exactly after
        the previous row has completely finished.
        """

        return (
            f"{current_time:.3f}s"
        )

    # ============================================================
    # Render
    # ============================================================

    def render(
        self,
        matrix,
        filename="ascii.svg",
    ):

        logger.info(
            "Rendering ASCII SVG"
        )

        # --------------------------------------------------------
        # Calculate document geometry
        # --------------------------------------------------------

        info = self.layout.calculate(
            matrix
        )

        box = info["box"]

        # --------------------------------------------------------
        # Transparent document
        # --------------------------------------------------------

        document = SVGDocument(

            width=info["width"],

            height=info["height"],

            background="transparent",

            # ----------------------------------------------------
            # IMPORTANT
            #
            # This changes only the external display size.
            #
            # The internal viewBox and all ASCII geometry
            # remain untouched.
            # ----------------------------------------------------

            display_width=ASCII_DISPLAY_WIDTH,

        )

        # --------------------------------------------------------
        # Embedded font
        # --------------------------------------------------------

        document.add_style(
            self.font.generate_style()
        )

        # --------------------------------------------------------
        # Typography metrics
        # --------------------------------------------------------

        glyph_width = (
            self.typography.glyph_width
        )

        glyph_height = (
            self.typography.glyph_height
        )

        padding = info["padding"]

        # --------------------------------------------------------
        # Visible matrix dimensions
        # --------------------------------------------------------

        visible_height = box.height

        # --------------------------------------------------------
        # Vertical mask height
        # --------------------------------------------------------

        row_height = (
            glyph_height
            + self.typography.font_size
        )

        # ========================================================
        # Cumulative animation timeline
        # ========================================================

        current_time = 0.0

        # --------------------------------------------------------
        # Counter
        # --------------------------------------------------------

        row_count = 0

        # ========================================================
        # Render one masked text block per row
        # ========================================================

        for local_y in range(
            visible_height
        ):

            matrix_y = (
                box.min_y
                + local_y
            )

            row = matrix[matrix_y]

            # ----------------------------------------------------
            # Crop row to visible bounding box.
            # ----------------------------------------------------

            visible_row = row[
                box.min_x:
                box.max_x + 1
            ]

            row_text = "".join(
                visible_row
            )

            # ----------------------------------------------------
            # Find actual visible characters.
            # ----------------------------------------------------

            visible_positions = [

                index

                for index, character
                in enumerate(row_text)

                if character != " "

            ]

            # ----------------------------------------------------
            # Completely empty row.
            # ----------------------------------------------------

            if not visible_positions:

                continue

            # ----------------------------------------------------
            # Actual first and last visible character.
            # ----------------------------------------------------

            first_visible = min(
                visible_positions
            )

            last_visible = max(
                visible_positions
            )

            # ----------------------------------------------------
            # Number of actual ASCII characters.
            # ----------------------------------------------------

            character_count = len(
                visible_positions
            )

            # ----------------------------------------------------
            # Actual horizontal span.
            # ----------------------------------------------------

            row_span = (
                last_visible
                - first_visible
                + 1
            )

            row_width = (
                row_span
                * glyph_width
            )

            # ----------------------------------------------------
            # SVG position
            # ----------------------------------------------------

            x = (
                padding
                + first_visible
                * glyph_width
            )

            y = (
                padding
                + self.typography.font_size
                + (
                    local_y
                    * glyph_height
                )
            )

            # ----------------------------------------------------
            # Mask vertical position
            # ----------------------------------------------------

            mask_y = (
                y
                - self.typography.font_size
            )

            # ----------------------------------------------------
            # Unique mask
            # ----------------------------------------------------

            mask_id = (
                f"ascii-row-mask-{local_y}"
            )

            # ====================================================
            # Dynamic duration
            # ====================================================

            duration_seconds = (
                self._row_duration(
                    character_count
                )
            )

            # ====================================================
            # Sequential start time
            # ====================================================

            begin = self._row_begin(
                current_time
            )

            # ----------------------------------------------------
            # Create mask
            # ----------------------------------------------------

            mask = SVGMaskReveal(

                id=mask_id,

                x=x,

                y=mask_y,

                width=row_width,

                height=row_height,

                direction="left",

                duration=(
                    f"{duration_seconds:.3f}s"
                ),

                begin=begin,

            )

            document.add_definition(
                mask
            )

            # ----------------------------------------------------
            # Keep original row structure.
            # ----------------------------------------------------

            block = SVGTextBlock(

                x=x,

                y=y,

                rows=[
                    row_text[
                        first_visible:
                        last_visible + 1
                    ]
                ],

                fill=(
                    self.typography.foreground
                ),

                font_family=(
                    self.typography.font_family
                ),

                font_size=(
                    self.typography.font_size
                ),

                line_height=(
                    self.typography.line_height
                ),

                font_weight=(
                    self.typography.font_weight
                ),

                letter_spacing=(
                    self.typography.letter_spacing
                ),

            )

            # ----------------------------------------------------
            # Attach mask
            # ----------------------------------------------------

            block.set_mask(
                mask_id
            )

            # ----------------------------------------------------
            # Add row
            # ----------------------------------------------------

            document.add(
                block
            )

            row_count += 1

            # ====================================================
            # Advance timeline.
            # ====================================================

            current_time += (
                duration_seconds
            )

        # ========================================================
        # Logging
        # ========================================================

        logger.info(
            f"ASCII Rows Rendered : "
            f"{row_count}"
        )

        logger.info(
            f"ASCII Reveal Duration : "
            f"{current_time:.3f}s"
        )

        # ========================================================
        # Save
        # ========================================================

        document.save(
            GENERATED_SVG / filename
        )

        logger.info(
            "ASCII SVG Complete"
        )