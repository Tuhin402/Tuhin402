from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# DIRECTORIES
# -------------------------------------------------

ASSETS = ROOT / "assets"

GENERATED = ROOT / "generated"

GENERATED_IMAGES = GENERATED / "images"

GENERATED_ASCII = GENERATED / "ascii"

GENERATED_SVG = GENERATED / "svg"

CACHE = ROOT / "cache"

LOGS = ROOT / "logs"

FONT_DIRECTORY = ASSETS / "fonts"

# -------------------------------------------------
# INPUTS
# -------------------------------------------------

PROFILE_IMAGE = ASSETS / "portrait-source.png"

# -------------------------------------------------
# IMAGE SETTINGS
# -------------------------------------------------

TARGET_SIZE = 1000

ASCII_WIDTH = 240

SAVE_DEBUG_IMAGES = True

CROP_PADDING = 40

# -------------------------------------------------
# ASCII SVG DISPLAY SETTINGS
# -------------------------------------------------

ASCII_DISPLAY_WIDTH = 720

# -------------------------------------------------
# SVG SETTINGS
# -------------------------------------------------

FONT_SIZE = 8

LINE_HEIGHT = 1.20

JETBRAINS_MONO = (
    FONT_DIRECTORY
    / "JetBrainsMono-Regular.ttf"
)