from pathlib import Path

from config.settings import ROOT

from scripts.generators.base import BaseGenerator

from scripts.utils.logger import logger


class ReadmeGenerator(BaseGenerator):
    """
    Generates the final README.md
    using the generated SVG assets.
    """

    def __init__(self):

        super().__init__()

    # --------------------------------------------------

    def generate(self):

        logger.info("=" * 60)
        logger.info("README GENERATOR")
        logger.info("=" * 60)

        content = self.build()

        output = ROOT / "README.md"

        output.write_text(
            content,
            encoding="utf-8",
        )

        logger.info("README.md generated.")

    # --------------------------------------------------

    def build(self):

        lines = []

        lines.append("# GitHub Profile")
        lines.append("")

        lines.append("## Profile")
        lines.append("")
        lines.append("![](generated/svg/ascii.svg)")
        lines.append("")

        lines.append("## Statistics")
        lines.append("")
        lines.append("![](generated/svg/stats.svg)")
        lines.append("")

        lines.append("## Languages")
        lines.append("")
        lines.append("![](generated/svg/languages.svg)")
        lines.append("")

        lines.append("## Contribution Calendar")
        lines.append("")
        lines.append("![](generated/svg/year.svg)")
        lines.append("")

        lines.append("## Contribution Streak")
        lines.append("")
        lines.append("![](generated/svg/streak.svg)")
        lines.append("")

        return "\n".join(lines)