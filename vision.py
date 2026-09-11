"""
EON Vision
==========
Visual perception layer for EON.

Capabilities:
- Image validation
- Image metadata inspection
- Image dimensions
- File information
- Vision input preparation
- Basic image analysis foundation

A real AI vision model can be connected later.
"""

from pathlib import Path


class Vision:
    """EON visual perception system."""

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

        self.last_image = None

        self.last_analysis = None

    # =========================================================
    # CHECK SUPPORTED FORMAT
    # =========================================================

    def is_supported(
        self,
        file_path
    ):

        path = Path(
            file_path
        )

        return (
            path.suffix.lower()
            in self.SUPPORTED_FORMATS
        )

    # =========================================================
    # CHECK IMAGE
    # =========================================================

    def inspect_image(
        self,
        file_path
    ):
        """Inspect an image before processing it."""

        path = Path(
            file_path
        )

        if not path.exists():

            return {
                "success": False,
                "error":
                    "Image not found.",
            }

        if not path.is_file():

            return {
                "success": False,
                "error":
                    "The selected path is not a file.",
            }

        if not self.is_supported(
            path
        ):

            return {
                "success": False,
                "error":
                    f"Unsupported image format: "
                    f"{path.suffix}",
            }

        result = {
            "success": True,

            "file":
                path.name,

            "path":
                str(path),

            "format":
                path.suffix.lower(),

            "size_bytes":
                path.stat().st_size,

            "status":
                "READY_FOR_ANALYSIS",
        }

        self.last_image = str(
            path
        )

        return result

    # =========================================================
    # IMAGE DIMENSIONS
    # =========================================================

    def get_dimensions(
        self,
        file_path
    ):
        """
        Read image dimensions.

        Uses the standard library where possible.
        Full pixel decoding can be connected through
        a vision/image library later.
        """

        inspection = self.inspect_image(
            file_path
        )

        if not inspection.get(
            "success",
            False
        ):

            return inspection

        try:

            with open(
                file_path,
                "rb"
            ) as image:

                header = image.read(
                    32
                )

            dimensions = (
                self._read_dimensions(
                    header
                )
            )

            if dimensions is None:

                return {
                    "success": False,
                    "error":
                        "Could not determine image dimensions.",
                }

            width, height = dimensions

            return {
                "success": True,
                "width": width,
                "height": height,
            }

        except OSError as error:

            return {
                "success": False,
                "error":
                    f"Unable to read image: {error}",
            }

    # =========================================================
    # DIMENSION PARSER
    # =========================================================

    def _read_dimensions(
        self,
        header
    ):
        """Read common image dimensions from file headers."""

        # -----------------------------------------------------
        # PNG
        # -----------------------------------------------------

        if header.startswith(
            b"\x89PNG\r\n\x1a\n"
        ):

            if len(header) >= 24:

                width = int.from_bytes(
                    header[16:20],
                    "big"
                )

                height = int.from_bytes(
                    header[20:24],
                    "big"
                )

                return width, height

        # -----------------------------------------------------
        # GIF
        # -----------------------------------------------------

        if header.startswith(
            (
                b"GIF87a",
                b"GIF89a",
            )
        ):

            if len(header) >= 10:

                width = int.from_bytes(
                    header[6:8],
                    "little"
                )

                height = int.from_bytes(
                    header[8:10],
                    "little"
                )

                return width, height

        # -----------------------------------------------------
        # BMP
        # -----------------------------------------------------

        if header.startswith(
            b"BM"
        ):

            if len(header) >= 26:

                width = int.from_bytes(
                    header[18:22],
                    "little",
                    signed=True
                )

                height = int.from_bytes(
                    header[22:26],
                    "little",
                    signed=True
                )

                return (
                    abs(width),
                    abs(height)
                )

        # -----------------------------------------------------
        # JPEG
        # -----------------------------------------------------

        if header.startswith(
            b"\xff\xd8"
        ):

            return self._jpeg_dimensions(
                header
            )

        return None

    # =========================================================
    # JPEG DIMENSIONS
    # =========================================================

    def _jpeg_dimensions(
        self,
        header
    ):
        """
        Attempt to read JPEG dimensions.

        A larger header may be required for some JPEG files,
        so this is primarily a lightweight foundation.
        """

        index = 2

        while index + 9 < len(header):

            if header[index] != 0xFF:

                index += 1
                continue

            marker = header[index + 1]

            # SOF markers
            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:

                height = int.from_bytes(
                    header[index + 5:index + 7],
                    "big"
                )

                width = int.from_bytes(
                    header[index + 7:index + 9],
                    "big"
                )

                return width, height

            if index + 4 >= len(header):

                break

            segment_length = int.from_bytes(
                header[index + 2:index + 4],
                "big"
            )

            if segment_length < 2:

                break

            index += (
                2 + segment_length
            )

        return None

    # =========================================================
    # PREPARE IMAGE
    # =========================================================

    def prepare(
        self,
        file_path,
        prompt=None
    ):
        """
        Prepare an image for a future AI vision model.
        """

        inspection = self.inspect_image(
            file_path
        )

        if not inspection.get(
            "success",
            False
        ):

            return inspection

        dimensions = self.get_dimensions(
            file_path
        )

        result = {
            "file":
                inspection["file"],

            "format":
                inspection["format"],

            "size_bytes":
                inspection["size_bytes"],

            "dimensions":
                dimensions,

            "prompt":
                prompt,

            "status":
                "READY_FOR_VISION_MODEL",
        }

        self.last_image = (
            inspection["path"]
        )

        return result

    # =========================================================
    # ANALYZE
    # =========================================================

    def analyze(
        self,
        file_path,
        prompt=None
    ):
        """
        Analyze an image.

        Currently returns structured information.
        A real AI vision model can be connected here later.
        """

        prepared = self.prepare(
            file_path,
            prompt
        )

        if (
            isinstance(
                prepared,
                dict
            )
            and prepared.get(
                "status"
            ) == "READY_FOR_VISION_MODEL"
        ):

            self.last_analysis = prepared

            return (
                "Vision input prepared successfully.\n"
                f"File: {prepared['file']}\n"
                f"Format: {prepared['format']}\n"
                f"Size: {prepared['size_bytes']} bytes\n"
                f"Prompt: "
                f"{prepared['prompt'] or 'General analysis'}\n"
                "AI vision model: not connected yet."
            )

        return prepared

    # =========================================================
    # LAST IMAGE
    # =========================================================

    def get_last_image(self):

        return self.last_image

    # =========================================================
    # LAST ANALYSIS
    # =========================================================

    def get_last_analysis(self):

        return self.last_analysis

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        return {
            "enabled":
                self.enabled,

            "status":
                self.status_state,

            "supported_formats":
                len(
                    self.SUPPORTED_FORMATS
                ),

            "last_image":
                self.last_image,

            "vision_model":
                "NOT_CONNECTED",
        }
