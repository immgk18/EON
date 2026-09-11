"""
EON Web Intelligence
====================
Web search and information retrieval foundation.
"""

from urllib.parse import quote
from urllib.request import Request, urlopen


class WebManager:
    """Handles basic web connectivity for EON."""

    def __init__(self):
        self.enabled = True
        self.status_state = "ONLINE"

    def create_search_url(self, query):
        """Create a search URL for a query."""

        if not query:
            return None

        encoded_query = quote(query)

        return f"https://www.google.com/search?q={encoded_query}"

    def check_connection(self):
        """Check whether internet connectivity is available."""

        try:
            request = Request(
                "https://www.google.com",
                headers={
                    "User-Agent": "EON/4.0"
                }
            )

            with urlopen(request, timeout=5):
                return True

        except Exception:
            return False

    def fetch_page(self, url):
        """
        Fetch basic text from a webpage.

        This is intentionally limited to simple retrieval.
        """

        if not url:
            return "No URL provided."

        try:
            request = Request(
                url,
                headers={
                    "User-Agent": "EON/4.0"
                }
            )

            with urlopen(request, timeout=10) as response:
                data = response.read()

            return data.decode(
                "utf-8",
                errors="ignore"
            )

        except Exception as error:
            return f"Unable to retrieve webpage: {error}"

    def status(self):
        """Return web system status."""

        connected = self.check_connection()

        return {
            "enabled": self.enabled,
            "status": self.status_state,
            "internet": connected,
        }
