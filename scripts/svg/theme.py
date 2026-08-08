from dataclasses import dataclass


@dataclass(frozen=True)
class SVGTheme:
    """
    Global theme used by every SVG.
    """

    # Backgrounds

    page_background: str = "#0D1117"
    container_background: str = "#0D1117"
    card_background: str = "#111111"

    # Text

    title: str = "#FFFFFF"
    subtitle: str = "#8B949E"
    body: str = "#C9D1D9"
    accent: str = "#58A6FF"
    success: str = "#3FB950"
    warning: str = "#D29922"
    danger: str = "#F85149"
    border: str = "#30363D"


DEFAULT_THEME = SVGTheme()