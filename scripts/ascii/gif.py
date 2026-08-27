from pathlib import Path
from typing import Sequence

from PIL import Image, ImageDraw

from config.settings import (
    GENERATED_GITHUB,
    GENERATED_SVG,
    ASCII_DISPLAY_WIDTH,
)

from scripts.svg.static_exporter import StaticSVGExporter


class ASCIIAnimatedGIFExporter:
    """
    Creates a GitHub-compatible animated GIF from the final
    appearance of the generated ASCII SVG.

    The final SVG is rasterized once, then each GIF frame uses
    inexpensive masking/compositing. This preserves the exact
    typography, proportions and colors of the SVG while keeping
    GIF generation practical.
    """

    def __init__(
        self,
        display_width=ASCII_DISPLAY_WIDTH,
        fps=8,
        duration_seconds=8.0,
    ):
        self.display_width = max(160, int(display_width))
        self.fps = max(4, min(10, int(fps)))
        self.duration_seconds = max(
            2.0,
            float(duration_seconds),
        )

    def _timeline(self, row_count):
        if row_count <= 0:
            return []

        # Slight variation keeps the reveal organic without
        # allowing any row to overlap another.
        weights = [
            0.82 + 0.18 * (
                i / max(1, row_count - 1)
            )
            for i in range(row_count)
        ]

        scale = (
            self.duration_seconds
            / sum(weights)
        )

        timeline = []
        current = 0.0

        for weight in weights:
            duration = (
                weight
                * scale
            )

            timeline.append(
                (
                    current,
                    current + duration,
                )
            )

            current += duration

        timeline[-1] = (
            timeline[-1][0],
            self.duration_seconds,
        )

        return timeline

    def _final_png(self, source_svg):
        """
        Freeze the SVG and rasterize it once.

        This uses the exact same final-state SVG representation
        that is intended for GitHub.
        """

        static_svg = (
            GENERATED_GITHUB
            / "_ascii-static.svg"
        )

        StaticSVGExporter().export(
            source_svg,
            static_svg,
        )

        import cairosvg

        png_bytes = cairosvg.svg2png(
            url=str(static_svg),
            output_width=self.display_width,
        )

        from io import BytesIO

        image = Image.open(
            BytesIO(png_bytes)
        ).convert("RGBA")

        return image

    def export_from_svg(
        self,
        source_svg=None,
        filename="ascii.gif",
        row_count=132,
    ):
        """
        Create the animated GIF from the generated ASCII SVG.

        row_count is supplied by the current ASCII bounding box.
        """

        if source_svg is None:
            source_svg = (
                GENERATED_SVG
                / "ascii.svg"
            )

        source_svg = Path(
            source_svg
        )

        if not source_svg.exists():
            raise FileNotFoundError(
                f"ASCII SVG not found: {source_svg}"
            )

        final_image = self._final_png(
            source_svg
        )

        width, height = final_image.size

        # The ASCII SVG's canvas is intentionally near-square.
        # Use each row as an animation band.
        band_height = max(
            1,
            height / max(1, row_count),
        )

        timeline = self._timeline(
            row_count
        )

        frame_count = max(
            2,
            int(
                round(
                    self.duration_seconds
                    * self.fps
                )
            ),
        )

        frames = []

        for frame_index in range(
            frame_count + 1
        ):

            elapsed = min(
                self.duration_seconds,
                frame_index / self.fps,
            )

            frame = Image.new(
                "RGBA",
                (width, height),
                (0, 0, 0, 0),
            )

            for row_index in range(
                row_count
            ):

                start, end = (
                    timeline[row_index]
                )

                if elapsed <= start:
                    continue

                if elapsed >= end:
                    progress = 1.0
                else:
                    progress = (
                        elapsed - start
                    ) / max(
                        0.001,
                        end - start,
                    )

                # Reveal the row left-to-right while the rows
                # themselves advance sequentially.
                y0 = int(
                    row_index * band_height
                )

                y1 = int(
                    (row_index + 1)
                    * band_height
                )

                visible_width = max(
                    1,
                    int(
                        width
                        * progress
                    ),
                )

                crop = final_image.crop(
                    (
                        0,
                        y0,
                        visible_width,
                        y1,
                    )
                )

                frame.alpha_composite(
                    crop,
                    (0, y0),
                )

            frames.append(
                frame.convert(
                    "P",
                    palette=Image.Palette.ADAPTIVE,
                    colors=128,
                )
            )

        destination = (
            GENERATED_GITHUB
            / filename
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        frames[0].save(
            destination,
            save_all=True,
            append_images=frames[1:],
            duration=int(
                round(
                    1000
                    / self.fps
                )
            ),
            loop=0,
            disposal=2,
            transparency=0,
            optimize=True,
        )

        static_svg = GENERATED_GITHUB / "_ascii-static.svg"

        try:
            static_svg.unlink()
        except OSError:
            pass

        return destination

    def export(
        self,
        matrix: Sequence[Sequence[str]],
        filename="ascii.gif",
    ):
        """
        Compatibility method used by ProfileGenerator.
        """

        from scripts.svg.bounding_box import BoundingBoxCalculator

        box = BoundingBoxCalculator().process(
            matrix
        )

        row_count = (
            box.height
        )

        return self.export_from_svg(
            row_count=row_count,
            filename=filename,
        )
