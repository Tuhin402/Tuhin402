import json
from pathlib import Path


class CacheSerializer:
    """
    Reads and writes cache files.
    """

    @staticmethod
    def save(path: Path, data):

        path.parent.mkdir(parents=True, exist_ok=True,)
        with open(path, "w", encoding="utf8",) as file:
            json.dump(data, file, indent=2,)

    # ---------------------------------------

    @staticmethod
    def load(path: Path):

        with open(path, "r", encoding="utf8",) as file:
            return json.load(file)