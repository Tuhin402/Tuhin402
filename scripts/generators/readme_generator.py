from config.settings import (
    GENERATED_GITHUB,
    GENERATED_SVG,
    PROFILE_BIO,
    PROFILE_DISPLAY_NAME,
    PROFILE_ROLE,
    PROFILE_SKILLS,
    README_ASSETS,
    README_IMAGE_WIDTHS,
    ROOT,
    ASCII_DISPLAY_WIDTH,
)

from scripts.generators.base import BaseGenerator
from scripts.svg.static_exporter import StaticSVGExporter
from scripts.utils.logger import logger

class ReadmeGenerator(BaseGenerator):
    """
    Generates the final GitHub profile README.

    The main ASCII portrait is referenced directly from:

        generated/svg/ascii.svg

    The remaining animated SVGs are exported as static
    final-state copies under:

        generated/github/

    This keeps the README GitHub-compatible while preserving
    the animated SVG source files for browser/local viewing.
    """

    def __init__(self):

        super().__init__()

        self.static_exporter = (
            StaticSVGExporter()
        )

    # ============================================================
    # Generate
    # ============================================================

    def generate(self):

        logger.info("=" * 60)

        logger.info(
            "README GENERATOR"
        )

        logger.info("=" * 60)

        self._generate_github_assets()

        self._remove_legacy_ascii_gif()

        content = self.build()

        output = (
            ROOT
            / "README.md"
        )

        output.write_text(
            content,
            encoding="utf-8",
        )

        logger.info(
            "README.md generated."
        )

    # ============================================================
    # GitHub Assets
    # ============================================================

    def _generate_github_assets(self):
        """
        Freeze the non-hero animated SVG assets at
        their final visual state for GitHub.
        """

        logger.info(
            "Generating GitHub static SVG assets..."
        )

        self.static_exporter.export_directory(

            source_directory=(
                GENERATED_SVG
            ),

            destination_directory=(
                GENERATED_GITHUB
            ),

            filenames=(
                README_ASSETS.keys()
            ),

        )

    # ============================================================
    # Legacy GIF Cleanup
    # ============================================================

    def _remove_legacy_ascii_gif(self):
        """
        Removes the old ASCII GIF if it exists.

        The project now uses ascii.svg directly.
        """

        legacy_gif = (
            GENERATED_GITHUB
            / "ascii.gif"
        )

        if not legacy_gif.exists():
            return

        try:

            legacy_gif.unlink()

            logger.info(
                "Removed legacy ascii.gif."
            )

        except OSError as error:

            logger.warning(
                f"Could not remove legacy ascii.gif: "
                f"{error}"
            )

    # ============================================================
    # Skill Icons
    # ============================================================

    def _skill_icon(
        self,
        skill,
    ):
        """
        Builds an icon-only technology item.
        """

        slug, color, label = skill

        return (
            f'<a '
            f'href="https://simpleicons.org/" '
            f'title="{label}">'
            f'<img '
            f'src="https://cdn.simpleicons.org/'
            f'{slug}/{color}" '
            f'alt="{label}" '
            f'width="42" '
            f'height="42">'
            f'</a>'
        )

    # ============================================================
    # Responsive Image Helper
    # ============================================================

    def _image(
        self,
        filename,
        alt,
        width,
    ):
        """
        Builds a centered responsive image block.
        """

        return [

            '<p align="center">',

            "",

            (
                f'<img '
                f'src="generated/github/{filename}" '
                f'alt="{alt}" '
                f'width="{width}">'
            ),

            "",

            '</p>',

        ]

    # ============================================================
    # Build README
    # ============================================================

    def build(self):

        lines = []

        # ========================================================
        # Hero
        # ========================================================

        lines.extend([

            '<div align="center">',

            "",

            (
                f'<img '
                f'src="generated/svg/ascii.svg" '
                f'width="{ASCII_DISPLAY_WIDTH}" '
                f'alt="ASCII profile portrait">'
            ),

            "",

            f'<h1>{PROFILE_DISPLAY_NAME}</h1>',

            "",

            (
                f'<p><strong>'
                f'{PROFILE_ROLE}'
                f'</strong></p>'
            ),

            "",

            (
                f'<p>'
                f'{PROFILE_BIO}'
                f'</p>'
            ),

            "",

            '</div>',

            "",

        ])

        # ========================================================
        # Skills
        # ========================================================

        lines.extend([

            '## ⚡ Skill Arsenal',

            "",

            '<div align="center">',

            "",

        ])

        for skill in PROFILE_SKILLS:

            lines.append(
                self._skill_icon(
                    skill
                )
            )

        lines.extend([

            "",

            '</div>',

            "",

            '<div align="center">',

            "",

            (
                '<sub>'
                '⚔️ Building with a full-stack toolkit — '
                'one release at a time.'
                '</sub>'
            ),

            "",

            '</div>',

            "",

        ])

        # ========================================================
        # GitHub Arena
        # ========================================================

        lines.extend([

            '## 🎮 GitHub Arena',

            "",

        ])

        lines.extend(

            self._image(

                filename="stats.svg",

                alt="GitHub statistics",

                width=(
                    README_IMAGE_WIDTHS[
                        "stats"
                    ]
                ),

            )

        )

        lines.append("")

        # ========================================================
        # Code DNA
        # ========================================================

        lines.extend([

            '## 🧬 Code DNA',

            "",

        ])

        lines.extend(

            self._image(

                filename="languages.svg",

                alt=(
                    "Programming language "
                    "distribution"
                ),

                width=(
                    README_IMAGE_WIDTHS[
                        "languages"
                    ]
                ),

            )

        )

        lines.append("")

        # ========================================================
        # Activity Garden
        # ========================================================

        lines.extend([

            '## 🌱 Activity Garden',

            "",

        ])

        lines.extend(

            self._image(

                filename="year.svg",

                alt=(
                    "GitHub contribution "
                    "calendar"
                ),

                width=(
                    README_IMAGE_WIDTHS[
                        "year"
                    ]
                ),

            )

        )

        lines.append("")

        # ========================================================
        # Streak
        # ========================================================

        lines.extend([

            '## 🔥 Streak',

            "",

        ])

        lines.extend(

            self._image(

                filename="streak.svg",

                alt=(
                    "GitHub contribution "
                    "streak"
                ),

                width=(
                    README_IMAGE_WIDTHS[
                        "streak"
                    ]
                ),

            )

        )

        lines.append("")

        # ========================================================
        # Footer
        # ========================================================

        lines.extend([

            '<div align="center">',

            "",

            (
                '<sub>'
                'Generated by a custom Python + SVG '
                'profile pipeline.'
                '</sub>'
            ),

            "",

            '</div>',

            "",

        ])

        return "\n".join(
            lines
        )