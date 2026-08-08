"""
Character ramps used by the ASCII renderer.

Characters are ordered from

DARKEST

↓

LIGHTEST
"""

# -----------------------------------------------------

STANDARD = (
    "$@B%8&WM#*oahkbdpqwm"
    "ZO0QLCJUYXzcvunxrjft/"
    r"\|()1{}[]?-_+~<>"
    'i!lI;:,"^`\' .'
)

# -----------------------------------------------------

BLOCKS = (
    "█▓▒░ "
)

# -----------------------------------------------------

SIMPLE = (
    "@%#*+=-:. "
)

# -----------------------------------------------------

MINIMAL = (
    "@#:. "
)

# -----------------------------------------------------

BRAILLE = (
    "⣿⣷⣶⣤⣀ "
)

# -----------------------------------------------------

RAMP_COLLECTION = {

    "standard": STANDARD,

    "blocks": BLOCKS,

    "simple": SIMPLE,

    "minimal": MINIMAL,

    "braille": BRAILLE,

}