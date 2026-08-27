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

    The animated SVGs remain under generated/svg for local/browser
    viewing. GitHub receives static final-state SVG copies under
    generated/github because GitHub does not support inline SVG
    animation or scripting.
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
        logger.info("README GENERATOR")
        logger.info("=" * 60)

        self._generate_github_assets()

        content = self.build()

        output = ROOT / "README.md"

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
        Freeze every animated SVG at its final visual state.
        """

        logger.info(
            "Generating GitHub static SVG assets..."
        )

        self.static_exporter.export_directory(
            source_directory=GENERATED_SVG,
            destination_directory=GENERATED_GITHUB,
            filenames=README_ASSETS.keys(),
        )

    # ============================================================
    # Skill Icons
    # ============================================================

    def _skill_icon(
        self,
        skill,
    ):
        """
        Build an icon-only Simple Icons image.

        The visible representation is only the vibrant icon.
        """

        slug, color, label = skill

        return (
            f'<a href="https://simpleicons.org/" '
            f'title="{label}">'
            f'<img '
            f'src="https://cdn.simpleicons.org/{slug}/{color}" '
            f'alt="{label}" '
            f'width="42" '
            f'height="42">'
            f'</a>'
        )

    # ============================================================
    # Image Helper
    # ============================================================

    def _image(
        self,
        filename,
        alt,
        width,
    ):
        """Build a centered, responsive image block."""

        return [
            '<p align="center">',
            '',
            f'<img '
            f'src="generated/github/{filename}" '
            f'alt="{alt}" '
            f'width="{width}">',
            '',
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
            '',
            f'<img '
            f'src="generated/github/ascii.gif" '
            f'width="{ASCII_DISPLAY_WIDTH}" '
            f'alt="Animated ASCII profile portrait">',
            '',
            f'<h1>{PROFILE_DISPLAY_NAME}</h1>',
            '',
            f'<p><strong>{PROFILE_ROLE}</strong></p>',
            '',
            f'<p>{PROFILE_BIO}</p>',
            '',
            '</div>',
            '',
        ])

        # ========================================================
        # Skills
        # ========================================================

        lines.extend([
            '## ⚡ Skill Arsenal',
            '',
            '<div align="center">',
            '',
        ])

        for skill in PROFILE_SKILLS:

            lines.append(
                self._skill_icon(skill)
            )

        lines.extend([
            '',
            '</div>',
            '',
            '<div align="center">',
            '',
            '<sub>⚔️ Building with a full-stack toolkit — one release at a time.</sub>',
            '',
            '</div>',
            '',
        ])

        # ========================================================
        # GitHub pulse
        # ========================================================

        lines.extend([
            '## 🎮 GitHub Arena',
            '',
        ])

        lines.extend(
            self._image(
                filename="stats.svg",
                alt="GitHub statistics",
                width=README_IMAGE_WIDTHS["stats"],
            )
        )

        lines.append('')

        # ========================================================
        # Languages
        # ========================================================

        lines.extend([
            '## 🧬 Code DNA',
            '',
        ])

        lines.extend(
            self._image(
                filename="languages.svg",
                alt="Programming language distribution",
                width=README_IMAGE_WIDTHS["languages"],
            )
        )

        lines.append('')

        # ========================================================
        # Contribution Calendar
        # ========================================================

        lines.extend([
            '## 🌱 Activity Garden',
            '',
        ])

        lines.extend(
            self._image(
                filename="year.svg",
                alt="GitHub contribution calendar",
                width=README_IMAGE_WIDTHS["year"],
            )
        )

        lines.append('')

        # ========================================================
        # Streak
        # ========================================================

        lines.extend([
            '## 🔥 Streak',
            '',
        ])

        lines.extend(
            self._image(
                filename="streak.svg",
                alt="GitHub contribution streak",
                width=README_IMAGE_WIDTHS["streak"],
            )
        )

        lines.append('')

        # ========================================================
        # Footer
        # ========================================================

        lines.extend([
            '<div align="center">',
            '',
            '<sub>Generated by a custom Python + SVG profile pipeline.</sub>',
            '',
            '</div>',
            '',
        ])

        return "\n".join(
            lines
        )
