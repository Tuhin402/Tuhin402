from scripts.ascii.ramps import RAMP_COLLECTION


class BrightnessMapper:

    """
    Maps pixel brightness to ASCII characters.
    """

    def __init__(

        self,

        ramp="standard",

    ):

        self.characters = RAMP_COLLECTION[ramp]

        self.max_index = len(self.characters) - 1

    # ---------------------------------------------

    def map_pixel(

        self,

        brightness,

    ):

        brightness = max(

            0,

            min(

                255,

                brightness,

            ),

        )

        index = int(

            brightness / 255

            * self.max_index

        )

        return self.characters[index]