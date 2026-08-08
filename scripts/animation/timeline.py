from dataclasses import dataclass


@dataclass
class TimelineStep:
    """
    Represents one animation
    start time.
    """

    name: str

    begin: float


class AnimationTimeline:
    """
    Controls the timing of
    all SVG animations.
    """

    def __init__(

        self,

        start=0.0,

        delay=0.20,

    ):

        self.current = start

        self.delay = delay

        self.steps = []

    # --------------------------------------------

    def add(

        self,

        name,

    ):

        step = TimelineStep(

            name=name,

            begin=self.current,

        )

        self.steps.append(step)

        self.current += self.delay

        return step

    # --------------------------------------------

    def reset(self):

        self.current = 0

        self.steps.clear()

    # --------------------------------------------

    def begin(

        self,

        name,

    ):

        for step in self.steps:

            if step.name == name:

                return f"{step.begin:.2f}s"

        return "0s"