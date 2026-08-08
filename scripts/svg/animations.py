from scripts.animation.smil import SMILAnimation


class SVGAnimationManager:
    """
    Stores animations for a single SVG element.
    """

    def __init__(self):

        self.animations = []

    # ---------------------------------------

    def add(self, animation: SMILAnimation,):

        self.animations.append(animation)

        return self

    # ---------------------------------------

    def render(self):

        return "\n".join(

            animation.render()

            for animation

            in self.animations

        )