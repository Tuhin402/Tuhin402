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

GENERATED_GITHUB = GENERATED / "github"

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

# The ASCII artwork keeps its internal aspect ratio.
# This controls only its rendered display width.
ASCII_DISPLAY_WIDTH = 520

# -------------------------------------------------
# PROFILE / README SETTINGS
# -------------------------------------------------

PROFILE_DISPLAY_NAME = "Tuhin"

PROFILE_ROLE = "Full Stack Web Developer"

PROFILE_BIO = (
    "Building polished web experiences, developer tooling, "
    "and practical systems with a focus on clean architecture "
    "and thoughtful UI."
)

PROFILE_SKILLS = (
    "PHP",
    "Laravel",
    "JavaScript",
    "React",
    "Node.js",
    "CSS",
    "GSAP",
    "MySQL",
)

README_IMAGE_WIDTHS = {
    "ascii": ASCII_DISPLAY_WIDTH,
    "stats": 860,
    "languages": 860,
    "year": 900,
    "streak": 736,
}

README_ASSETS = {
    "ascii.svg": "ascii.svg",
    "stats.svg": "stats.svg",
    "languages.svg": "languages.svg",
    "year.svg": "year.svg",
    "streak.svg": "streak.svg",
}

# -------------------------------------------------
# SVG SETTINGS
# -------------------------------------------------

FONT_SIZE = 8

LINE_HEIGHT = 1.20

JETBRAINS_MONO = (
    FONT_DIRECTORY
    / "JetBrainsMono-Regular.ttf"
)
