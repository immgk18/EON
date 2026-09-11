"""
EON Vision
==========
Visual perception layer for EON.
"""

from pathlib import Path


class Vision:
    """Handles visual input for EON."""

    SUPPORTED_FORMATS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
        ".gif",
    }

    def __init__(self):
        self.enabled = True
        self.status_state = "READY"

    def is_supported(self, file_path):
        """Check whether an image format is supported."""

        path = Path(file_path)

        return path.suffix.lower() in self.SUPPORTED_FORMATS

    def inspect_image(self, file_path):
        """
        Inspect an image.

        Actual AI vision processing will be connected later.
        """

        path = Path(file_path)

        if not path.exists():
            return "Image not found."

        if not path.is_file():
            return "The selected path is not an image file."

        if not self.is_supported(path):
            return (
                f"Unsupported image format: {path.suffix}"
            )

        return {
            "file": path.name,
            "format": path.suffix.lower(),
            "size": path.stat().st_size,
            "status": "READY_FOR_ANALYSIS",
        }

    def analyze(self, file_path, prompt=None):
        """
        Analyze an image using the future vision engine.
        """

        inspection = self.inspect_image(file_path)

        if isinstance(inspection, str):
            return inspection

        if prompt:
            return (
                f"Vision input received for '{path_name(file_path)}'. "
                f"Requested analysis: {prompt}"
            )

        return (
            f"Vision input received for '{path_name(file_path)}'. "
            "Actual visual analysis engine is ready to be connected."
        )

    def status(self):
        """Return vision system status."""

        return {
            "enabled": self.enabled,
            "status": self.status_state,
            "supported_formats": len(self.SUPPORTED_FORMATS),
        }


def path_name(file_path):
    """Return the filename from a path."""

    return Path(file_path).name
