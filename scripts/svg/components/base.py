from abc import ABC
from abc import abstractmethod


class SVGComponent(ABC):
    """
    Base class for every SVG component.

    Every reusable SVG element
    inherits from this class.
    """

    def __init__(self):

        super().__init__()

    # ------------------------------------------------

    @abstractmethod
    def render(self):
        """
        Returns SVG elements.

        The return value can be

        SVGElement

        or

        list[SVGElement]
        """

        raise NotImplementedError