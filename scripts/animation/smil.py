from dataclasses import dataclass
from typing import Optional

from scripts.animation.easing import Easing
from scripts.animation.easing import Easings


# ============================================================
# Base Animation
# ============================================================

@dataclass
class SMILAnimation:
    """
    Base class for every
    SVG SMIL animation.
    """

    duration: str = "0.8s"
    begin: str = "0s"

    fill: str = "freeze"
    repeat_count: str = "1"

    calc_mode: str = "spline"

    easing: Optional[Easing] = Easings.EASE

    # ------------------------------------------------

    @property
    def key_splines(self):

        if self.easing:

            return self.easing.spline

        return "0.25 0.1 0.25 1"

    # ------------------------------------------------

    def render(self):

        raise NotImplementedError


# ============================================================
# Normal Attribute Animation
# ============================================================

@dataclass
class Animate(SMILAnimation):

    attribute_name: str = ""
    from_value: str = ""
    to_value: str = ""

    # ------------------------------------------------

    def render(self):

        return (

            f'<animate '
            f'attributeName="{self.attribute_name}" '
            f'from="{self.from_value}" '
            f'to="{self.to_value}" '
            f'dur="{self.duration}" '
            f'begin="{self.begin}" '
            f'fill="{self.fill}" '
            f'repeatCount="{self.repeat_count}" '
            f'calcMode="{self.calc_mode}" '
            f'keySplines="{self.key_splines}" '
            f'keyTimes="0;1" />'

        )


# ============================================================
# Transform Animation
# ============================================================

@dataclass
class AnimateTransform(SMILAnimation):

    transform_type: str = "translate"

    from_value: str = "0 0"
    to_value: str = "0 0"

    additive: str = "sum"

    # ------------------------------------------------

    def render(self):

        return (

            f'<animateTransform '
            f'attributeName="transform" '
            f'attributeType="XML" '
            f'type="{self.transform_type}" '
            f'from="{self.from_value}" '
            f'to="{self.to_value}" '
            f'dur="{self.duration}" '
            f'begin="{self.begin}" '
            f'fill="{self.fill}" '
            f'additive="{self.additive}" '
            f'calcMode="{self.calc_mode}" '
            f'keySplines="{self.key_splines}" '
            f'keyTimes="0;1" />'

        )


# ============================================================
# Opacity Animation
# ============================================================

@dataclass
class AnimateOpacity(Animate):

    attribute_name: str = "opacity"

    from_value: str = "0"

    to_value: str = "1"