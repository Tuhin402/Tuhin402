from pathlib import Path
import xml.etree.ElementTree as ET

from scripts.utils.logger import logger


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NAMESPACE)


class StaticSVGExporter:
    """
    Converts an animated SVG into a static final-state SVG.

    This exists specifically for GitHub README rendering.

    GitHub supports SVG images but does not support inline SVG
    animation or scripting. The animated SVGs remain available
    under generated/svg for direct browser/local viewing, while
    this exporter creates final-state copies under generated/github.

    The exporter evaluates the final `to` value of SVG animation
    elements and removes the animation nodes.
    """

    ANIMATION_TAGS = {
        "animate",
        "animateTransform",
        "animateMotion",
        "set",
    }

    def export(
        self,
        source,
        destination,
    ):
        """
        Export one animated SVG as a static final-state SVG.
        """

        source = Path(source)
        destination = Path(destination)

        if not source.exists():
            raise FileNotFoundError(
                f"SVG source not found: {source}"
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        tree = ET.parse(source)
        root = tree.getroot()

        self._freeze_tree(root)

        tree.write(
            destination,
            encoding="utf-8",
            xml_declaration=True,
        )

        logger.info(
            f"Static SVG Saved : {destination.name}"
        )

        return destination

    # ------------------------------------------------------------

    def export_directory(
        self,
        source_directory,
        destination_directory,
        filenames,
    ):
        """
        Export a collection of SVG files.
        """

        source_directory = Path(
            source_directory
        )

        destination_directory = Path(
            destination_directory
        )

        results = []

        for filename in filenames:

            results.append(
                self.export(
                    source_directory / filename,
                    destination_directory / filename,
                )
            )

        return results

    # ------------------------------------------------------------

    def _freeze_tree(self, element):
        """
        Recursively apply the final value of animations.
        """

        animation_children = []

        for child in list(element):

            local_name = self._local_name(
                child.tag
            )

            if local_name in self.ANIMATION_TAGS:

                animation_children.append(
                    child
                )

                self._apply_final_value(
                    element,
                    child,
                )

                continue

            self._freeze_tree(
                child
            )

        for child in animation_children:

            element.remove(
                child
            )

        # --------------------------------------------------------
        # CSS animation cannot be relied on by GitHub.
        # Static SVGs are already in their final visual state,
        # so we intentionally leave CSS declarations harmless.
        # --------------------------------------------------------

        if element.get("opacity") == "0":

            # A zero opacity on a non-animated element should
            # remain untouched. Animated opacity elements have
            # already been updated by _apply_final_value().
            pass

    # ------------------------------------------------------------

    def _apply_final_value(
        self,
        element,
        animation,
    ):
        """
        Applies an animation's final state to its parent.
        """

        local_name = self._local_name(
            animation.tag
        )

        if local_name == "animate":

            attribute_name = animation.get(
                "attributeName"
            )

            if not attribute_name:
                return

            to_value = animation.get(
                "to"
            )

            if to_value is None:

                values = animation.get(
                    "values"
                )

                if values:
                    to_value = values.split(";")[-1].strip()

            if to_value is None:
                return

            element.set(
                attribute_name,
                to_value,
            )

            return

        if local_name == "animateTransform":

            to_value = animation.get(
                "to"
            )

            if to_value is None:
                return

            transform_type = animation.get(
                "type",
                "transform",
            )

            element.set(
                "transform",
                f"{transform_type}({to_value})",
            )

            return

        if local_name == "set":

            attribute_name = animation.get(
                "attributeName"
            )

            to_value = animation.get(
                "to"
            )

            if attribute_name and to_value is not None:

                element.set(
                    attribute_name,
                    to_value,
                )

    # ------------------------------------------------------------

    @staticmethod
    def _local_name(tag):

        if "}" in tag:
            return tag.rsplit("}", 1)[-1]

        return tag
