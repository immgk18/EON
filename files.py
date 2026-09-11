"""
EON File System
===============
Safe file inspection and reading layer for EON.
"""

from pathlib import Path


class FileManager:
    """Handles basic file operations for EON."""

    def __init__(self, base_directory="."):
        self.base_directory = Path(base_directory).resolve()

    def _safe_path(self, path):
        """Resolve a path and keep it inside the allowed directory."""

        target = (self.base_directory / path).resolve()

        try:
            target.relative_to(self.base_directory)
        except ValueError:
            raise PermissionError(
                "Access outside the allowed directory is not permitted."
            )

        return target

    def exists(self, path):
        """Check whether a file or folder exists."""

        target = self._safe_path(path)
        return target.exists()

    def list_files(self, path="."):
        """List files and folders in an allowed directory."""

        target = self._safe_path(path)

        if not target.exists():
            return []

        if not target.is_dir():
            return []

        return [
            item.name
            for item in target.iterdir()
        ]

    def read_file(self, path, encoding="utf-8"):
        """Read a text file."""

        target = self._safe_path(path)

        if not target.exists():
            return "File not found."

        if not target.is_file():
            return "The selected path is not a file."

        try:
            return target.read_text(encoding=encoding)

        except UnicodeDecodeError:
            return "This file is not a supported text file."

        except OSError as error:
            return f"Unable to read file: {error}"

    def file_info(self, path):
        """Return basic information about a file."""

        target = self._safe_path(path)

        if not target.exists():
            return None

        return {
            "name": target.name,
            "path": str(target),
            "type": "directory" if target.is_dir() else "file",
            "size": target.stat().st_size,
        }

    def status(self):
        """Return file system manager status."""

        return {
            "status": "ONLINE",
            "base_directory": str(self.base_directory),
        }
