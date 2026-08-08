from dataclasses import dataclass, field
from xml.sax.saxutils import escape
from xml.sax.saxutils import quoteattr

from scripts.svg.animations import SVGAnimationManager


# ============================================================
# Base Element
# ============================================================

@dataclass
class SVGElement:
    """
    Base class for every SVG element.

    Provides:

    - animation support
    - reusable SVG attributes
    - mask support
    - clip-path support
    - filter support
    - opacity support
    - id / class support

    Existing SVG element constructors remain unchanged.
    """

    animations: SVGAnimationManager = field(
        default_factory=SVGAnimationManager,
        init=False,
        repr=False,
    )

    # --------------------------------------------------------
    # Animation
    # --------------------------------------------------------

    def animate(self, animation):
        """
        Attach an animation to this SVG element.
        """

        self.animations.add(animation)

        return self

    # --------------------------------------------------------

    def render_animations(self):

        return self.animations.render()

    # ========================================================
    # SVG Attributes
    # ========================================================

    def _svg_attributes(self):

        attributes = getattr(
            self,
            "_custom_svg_attributes",
            None,
        )

        if attributes is None:

            attributes = {}

            self._custom_svg_attributes = attributes

        return attributes

    # --------------------------------------------------------

    def set_attribute(
        self,
        name,
        value,
    ):
        """
        Add or replace a custom SVG attribute.

        Example:

            element.set_attribute(
                "data-type",
                "profile",
            )
        """

        self._svg_attributes()[name] = str(value)

        return self

    # --------------------------------------------------------

    def set_id(self, value):
        """
        Set the SVG element id.
        """

        return self.set_attribute(
            "id",
            value,
        )

    # --------------------------------------------------------

    def set_class(self, value):
        """
        Set the SVG class attribute.
        """

        return self.set_attribute(
            "class",
            value,
        )

    # --------------------------------------------------------

    def set_mask(self, mask):
        """
        Apply an SVG mask.

        Accepts either:

            "profile-mask"

        or:

            "url(#profile-mask)"
        """

        if mask is None:

            return self

        mask = str(mask)

        if not mask.startswith("url("):

            mask = f"url(#{mask})"

        return self.set_attribute(
            "mask",
            mask,
        )

    # --------------------------------------------------------

    def set_clip_path(self, clip_path):
        """
        Apply an SVG clip path.

        Accepts either:

            "profile-clip"

        or:

            "url(#profile-clip)"
        """

        if clip_path is None:

            return self

        clip_path = str(clip_path)

        if not clip_path.startswith("url("):

            clip_path = f"url(#{clip_path})"

        return self.set_attribute(
            "clip-path",
            clip_path,
        )

    # --------------------------------------------------------

    def set_filter(self, filter_id):
        """
        Apply an SVG filter.

        Accepts either:

            "profile-glow"

        or:

            "url(#profile-glow)"
        """

        if filter_id is None:

            return self

        filter_id = str(filter_id)

        if not filter_id.startswith("url("):

            filter_id = f"url(#{filter_id})"

        return self.set_attribute(
            "filter",
            filter_id,
        )

    # --------------------------------------------------------

    def set_opacity(self, opacity):
        """
        Set element opacity.
        """

        opacity = max(
            0.0,
            min(
                1.0,
                float(opacity),
            ),
        )

        return self.set_attribute(
            "opacity",
            opacity,
        )

    # --------------------------------------------------------

    def set_visibility(self, visibility):
        """
        Set SVG visibility.

        Examples:

            visible
            hidden
        """

        return self.set_attribute(
            "visibility",
            visibility,
        )

    # --------------------------------------------------------

    def render_custom_attributes(self):
        """
        Converts custom SVG attributes into XML attributes.

        Custom attributes are rendered exactly once.

        This method is intentionally kept generic so that
        existing SVG elements and future components can
        safely attach attributes such as:

            opacity
            mask
            clip-path
            filter
            id
            class
        """

        attributes = self._svg_attributes()

        if not attributes:
            return ""

        rendered = []

        for name, value in attributes.items():

            rendered.append(
                f"{name}={quoteattr(str(value))}"
            )

        return " ".join(rendered)

    # ========================================================
    # Render
    # ========================================================

    def render(self):

        raise NotImplementedError


# ============================================================
# Rectangle
# ============================================================

@dataclass
class SVGRect(SVGElement):

    x: float
    y: float

    width: float
    height: float

    fill: str = "#000000"

    stroke: str | None = None
    stroke_width: float = 0

    rx: float = 0
    ry: float = 0

    # --------------------------------------------------------

    def render(self):

        animation = self.render_animations()

        attributes = [

            f'x="{self.x}"',
            f'y="{self.y}"',

            f'width="{self.width}"',
            f'height="{self.height}"',

            f'fill="{self.fill}"',

            f'rx="{self.rx}"',
            f'ry="{self.ry}"',

        ]

        # ----------------------------------------------------
        # Stroke
        # ----------------------------------------------------

        if self.stroke is not None:

            attributes.append(
                f'stroke="{self.stroke}"'
            )

        if self.stroke_width > 0:

            attributes.append(
                f'stroke-width="{self.stroke_width}"'
            )

        # ----------------------------------------------------
        # Custom SVG attributes
        # ----------------------------------------------------

        custom = self.render_custom_attributes()

        if custom:

            attributes.append(custom)

        attributes = " ".join(attributes)

        # ----------------------------------------------------
        # Animated rectangle
        # ----------------------------------------------------

        if animation:

            return (
                f'<rect {attributes}>'
                f'{animation}'
                f'</rect>'
            )

        # ----------------------------------------------------
        # Static rectangle
        # ----------------------------------------------------

        return (
            f'<rect '
            f'{attributes} />'
        )


# ============================================================
# Text
# ============================================================

@dataclass
class SVGText(SVGElement):

    x: float
    y: float

    value: str
    fill: str

    font_family: str
    font_size: int

    font_weight: str = "400"
    letter_spacing: float = 0

    # --------------------------------------------------------

    def render(self):

        animation = self.render_animations()

        attributes = [

            f'x="{self.x}"',
            f'y="{self.y}"',

            f'fill="{self.fill}"',

            f'font-family="{self.font_family}"',

            f'font-size="{self.font_size}"',

            f'font-weight="{self.font_weight}"',

            f'letter-spacing="{self.letter_spacing}"',

            'xml:space="preserve"',
        ]

        # ----------------------------------------------------
        # Custom SVG attributes
        # ----------------------------------------------------

        custom = self.render_custom_attributes()

        if custom:

            attributes.append(custom)

        attributes = " ".join(attributes)

        value = escape(
            self.value
        )

        # ----------------------------------------------------
        # Animated text
        # ----------------------------------------------------

        if animation:

            return (
                f'<text '
                f'{attributes}>'
                f'{value}'
                f'{animation}'
                f'</text>'
            )

        # ----------------------------------------------------
        # Static text
        # ----------------------------------------------------

        return (
            f'<text '
            f'{attributes}>'
            f'{value}'
            f'</text>'
        )


# ============================================================
# Text Block
# ============================================================

@dataclass
class SVGTextBlock(SVGElement):
    """
    Represents multiple ASCII rows rendered
    as a single <text> element with multiple
    <tspan> children.

    Supports all SVGElement features:

    - animations
    - masks
    - filters
    - clip paths
    - opacity
    - id
    - class
    """

    x: float
    y: float

    rows: list[str]

    fill: str

    font_family: str
    font_size: int

    line_height: float

    font_weight: str = "400"

    letter_spacing: float = 0

    # --------------------------------------------------------

    def render(self):

        animation = self.render_animations()

        attributes = [

            f'x="{self.x}"',
            f'y="{self.y}"',

            f'fill="{self.fill}"',

            f'font-family="{self.font_family}"',

            f'font-size="{self.font_size}"',

            f'font-weight="{self.font_weight}"',

            f'letter-spacing="{self.letter_spacing}"',

            'xml:space="preserve"',
        ]

        # ----------------------------------------------------
        # Custom SVG attributes
        # ----------------------------------------------------

        custom = self.render_custom_attributes()

        if custom:

            attributes.append(custom)

        attributes = " ".join(attributes)

        svg = []

        # ----------------------------------------------------
        # Text opening
        # ----------------------------------------------------

        svg.append(

            f'<text '
            f'{attributes}>'

        )

        # ----------------------------------------------------
        # Rows
        # ----------------------------------------------------

        for index, row in enumerate(self.rows):

            dy = (
                0
                if index == 0
                else self.line_height
            )

            svg.append(

                f'<tspan '
                f'x="{self.x}" '
                f'dy="{dy}em">'

                f'{escape(row)}'

                f'</tspan>'

            )

        # ----------------------------------------------------
        # Animations
        # ----------------------------------------------------

        if animation:

            svg.append(
                animation
            )

        # ----------------------------------------------------
        # Close text
        # ----------------------------------------------------

        svg.append(
            "</text>"
        )

        return "\n".join(svg)




# ============================================================
# Character Reveal
# ============================================================

@dataclass
class SVGCharacterText(SVGElement):
    """
    Represents one ASCII character.

    Each visible character can have its own
    animation timing, allowing the ASCII portrait
    to reveal organically instead of appearing
    row-by-row like a scanner.
    """

    x: float
    y: float

    value: str
    fill: str

    font_family: str
    font_size: int

    font_weight: str = "400"
    letter_spacing: float = 0

    # --------------------------------------------------------

    def render(self):

        animation = self.render_animations()

        attributes = [

            f'x="{self.x}"',
            f'y="{self.y}"',

            f'fill="{self.fill}"',

            f'font-family="{self.font_family}"',

            f'font-size="{self.font_size}"',

            f'font-weight="{self.font_weight}"',

            f'letter-spacing="{self.letter_spacing}"',

            'xml:space="preserve"',
        ]

        # ----------------------------------------------------
        # Custom SVG attributes
        # ----------------------------------------------------

        custom = self.render_custom_attributes()

        if custom:
            attributes.append(custom)

        attributes = " ".join(attributes)

        value = escape(self.value)

        # ----------------------------------------------------
        # Animated character
        # ----------------------------------------------------

        if animation:

            return (
                f'<text '
                f'{attributes}>'
                f'{value}'
                f'{animation}'
                f'</text>'
            )

        # ----------------------------------------------------
        # Static character
        # ----------------------------------------------------

        return (
            f'<text '
            f'{attributes}>'
            f'{value}'
            f'</text>'
        )