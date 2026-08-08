import json
from pathlib import Path

from config.settings import GENERATED_ASCII
from scripts.utils.logger import logger


class ASCIIRenderer:

    """
    Responsible only for writing
    ASCII output to disk.

    It does NOT generate ASCII.

    It only renders it.
    """

    def __init__(self):

        GENERATED_ASCII.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------

    def render_text(

        self,

        matrix,

        filename="ascii.txt",

    ):

        output = GENERATED_ASCII / filename

        with open(

            output,

            "w",

            encoding="utf8",

        ) as file:

            for row in matrix:

                file.write(

                    "".join(row)

                )

                file.write("\n")

        logger.info(

            f"ASCII Text -> {output.name}"

        )

    # ---------------------------------------------

    def render_json(

        self,

        matrix,

        filename="ascii_matrix.json",

    ):

        output = GENERATED_ASCII / filename

        with open(

            output,

            "w",

            encoding="utf8",

        ) as file:

            json.dump(

                matrix,

                file,

                indent=2,

                ensure_ascii=False,

            )

        logger.info(

            f"ASCII JSON -> {output.name}"

        )

    # ---------------------------------------------

    def render(

        self,

        matrix,

    ):

        self.render_text(matrix)

        self.render_json(matrix)