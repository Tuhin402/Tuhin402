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

# Controls only the rendered width of the ASCII
# portrait. Internal ASCII geometry is unchanged.
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

# Icon-only skill stack used by the generated README.
# slug is the Simple Icons CDN slug and color is the icon brand color.
PROFILE_SKILLS = (
    ("php", "777BB4", "PHP"),
    ("laravel", "FF2D20", "Laravel"),
    ("javascript", "F7DF1E", "JavaScript"),
    ("react", "61DAFB", "React"),
    ("nodedotjs", "339933", "Node.js"),
    ("nextdotjs", "FFFFFF", "Next.js"),
    ("python", "3776AB", "Python"),
    ("tailwindcss", "06B6D4", "Tailwind CSS"),
    ("bootstrap", "7952B3", "Bootstrap"),
    ("postgresql", "4169E1", "PostgreSQL"),
    ("mysql", "4479A1", "MySQL"),
    ("greensock", "88CE02", "GSAP"),
)

README_IMAGE_WIDTHS = {
    "stats": 860,
    "languages": 860,
    "year": 900,
    "streak": 736,
}

README_ASSETS = {
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

ASCII_RAMP_STANDARD = (
    "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/"
    "|()1{}[]?-_+~<>i!lI;:,\"^`'. "
)

ASCII_RAMP_SIMPLE = "@%#*+=-:. "

DEFAULT_BACKGROUND = "#000000"

DEFAULT_FOREGROUND = "#FFFFFF"

DEFAULT_FONT = "JetBrains Mono"
