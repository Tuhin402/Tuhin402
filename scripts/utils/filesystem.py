from pathlib import Path

from config.settings import (
    GENERATED,
    GENERATED_IMAGES,
    GENERATED_ASCII,
    GENERATED_SVG,
    CACHE,
    LOGS,
)

DIRECTORIES = [
    GENERATED,
    GENERATED_IMAGES,
    GENERATED_ASCII,
    GENERATED_SVG,
    CACHE,
    LOGS,
]


def ensure_directories():
    """
    Create every directory required by the project.
    """

    for directory in DIRECTORIES:
        Path(directory).mkdir(parents=True, exist_ok=True)