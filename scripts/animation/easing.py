from dataclasses import dataclass


@dataclass(frozen=True)
class Easing:

    """
    Represents one SMIL easing curve.
    """

    name: str
    spline: str


class Easings:
    """
    Collection of reusable easing curves.
    """

    LINEAR = Easing(

        "linear",
        "0 0 1 1",

    )

    EASE = Easing(

        "ease",
        "0.25 0.1 0.25 1",

    )

    EASE_IN = Easing(

        "ease-in",
        "0.42 0 1 1",

    )

    EASE_OUT = Easing(

        "ease-out",
        "0 0 0.58 1",

    )

    EASE_IN_OUT = Easing(

        "ease-in-out",
        "0.42 0 0.58 1",

    )

    FAST_OUT = Easing(

        "fast-out",
        "0.4 0 1 1",

    )

    SLOW_IN = Easing(

        "slow-in",
        "0 0 0.2 1",

    )