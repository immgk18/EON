"""
EON Web Intelligence
====================
Web search and information retrieval layer for EON.

Capabilities:
- Create search URLs
- Check internet connectivity
- Fetch webpages
- Extract basic readable text
- Search and retrieve pages
- Return structured results
"""

import re
from html import unescape
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class WebManager:
    """Manages EON's web-intelligence capabilities."""

    SEARCH_ENGINE = (
        "https://www.google.com/search?q="
    )

    USER_AGENT = (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "EON/4.0"
    )

    def __init__(self):

        self.enabled = True
        self.status_state = "ONLINE"

        self.timeout = 10

        self.last_url = None
        self.last_result = None

    # =========================================================
    # CREATE SEARCH URL
    # =========================================================

    def create_search_url(self, query):
        """Create a search-engine URL."""

        if not query:
            return None

        query = query.strip()

        encoded_query = quote(
            query
        )

        return (
            f"{self.SEARCH_ENGINE}"
            f"{encoded_query}"
        )

    # =========================================================
    # CHECK CONNECTION
    # =========================================================

    def check_connection(self):
        """Check whether internet access is available."""

        try:

            request = Request(
                "https://www.google.com",
                headers={
                    "User-Agent":
                        self.USER_AGENT
                }
            )

            with urlopen(
                request,
                timeout=5
            ):

                return True

        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
        ):

            return False

    # =========================================================
    # FETCH PAGE
    # =========================================================

    def fetch_page(self, url):
        """Retrieve raw webpage content."""

        if not url:

            return (
                "No URL provided."
            )

        if not self._is_http_url(url):

            return (
                "Only HTTP and HTTPS URLs "
                "are supported."
            )

        try:

            request = Request(
                url,
                headers={
                    "User-Agent":
                        self.USER_AGENT
                }
            )

            with urlopen(
                request,
                timeout=self.timeout
            ) as response:

                data = response.read()

                content_type = (
                    response.headers.get(
                        "Content-Type",
                        ""
                    )
                )

            self.last_url = url

            # -------------------------------------------------
            # Decode content
            # -------------------------------------------------

            encoding = self._get_encoding(
                content_type
            )

            text = data.decode(
                encoding,
                errors="ignore"
            )

            self.last_result = text

            return text

        except HTTPError as error:

            return (
                f"HTTP error {error.code}: "
                f"{error.reason}"
            )

        except URLError as error:

            return (
                f"Unable to reach webpage: "
                f"{error.reason}"
            )

        except TimeoutError:

            return (
                "Web request timed out."
            )

        except OSError as error:

            return (
                f"Web request failed: "
                f"{error}"
            )

    # =========================================================
    # GET ENCODING
    # =========================================================

    def _get_encoding(
        self,
        content_type
    ):

        match = re.search(
            r"charset=([a-zA-Z0-9_-]+)",
            content_type
        )

        if match:

            return match.group(1)

        return "utf-8"

    # =========================================================
    # HTML TO TEXT
    # =========================================================

    def extract_text(
        self,
        html
    ):
        """Convert basic HTML into readable text."""

        if not html:

            return ""

        text = html

        # Remove scripts
        text = re.sub(
            r"<script\b[^>]*>.*?</script>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        # Remove styles
        text = re.sub(
            r"<style\b[^>]*>.*?</style>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        # Remove comments
        text = re.sub(
            r"<!--.*?-->",
            " ",
            text,
            flags=re.DOTALL
        )

        # Replace common block elements
        text = re.sub(
            r"</(p|div|section|article|br|li|h[1-6])>",
            "\n",
            text,
            flags=re.IGNORECASE
        )

        # Remove remaining HTML tags
        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        # Decode HTML entities
        text = unescape(
            text
        )

        # Normalize whitespace
        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        text = re.sub(
            r"\n\s*\n+",
            "\n\n",
            text
        )

        return text.strip()

    # =========================================================
    # FETCH READABLE TEXT
    # =========================================================

    def fetch_text(self, url):
        """Fetch a webpage and return readable text."""

        html = self.fetch_page(
            url
        )

        if not html:
            return ""

        if html.startswith(
            (
                "HTTP error",
                "Unable to reach",
                "Web request",
                "Only HTTP",
                "No URL",
            )
        ):

            return html

        return self.extract_text(
            html
        )

    # =========================================================
    # SEARCH
    # =========================================================

    def search(self, query):
        """
        Prepare a web search.

        The current foundation returns a search URL.
        A dedicated search API/parser can be connected later.
        """

        if not query:

            return {
                "success": False,
                "query": "",
                "url": None,
                "message":
                    "No search query provided.",
            }

        url = self.create_search_url(
            query
        )

        self.last_url = url

        return {
            "success": True,
            "query": query.strip(),
            "url": url,
            "message":
                "Search request prepared.",
        }

    # =========================================================
    # OPEN SEARCH RESULT PAGE
    # =========================================================

    def search_page(
        self,
        query
    ):
        """
        Fetch the search-engine results page.

        This is primarily a foundation for future
        result extraction.
        """

        url = self.create_search_url(
            query
        )

        if not url:

            return (
                "No search query provided."
            )

        return self.fetch_text(
            url
        )

    # =========================================================
    # EXTRACT LINKS
    # =========================================================

    def extract_links(
        self,
        html,
        limit=10
    ):
        """Extract basic HTTP/HTTPS links from HTML."""

        if not html:

            return []

        links = []

        pattern = (
            r'href=["\']'
            r'(https?://[^"\']+)'
            r'["\']'
        )

        matches = re.findall(
            pattern,
            html,
            flags=re.IGNORECASE
        )

        for url in matches:

            if url not in links:

                links.append(
                    url
                )

            if len(links) >= limit:

                break

        return links

    # =========================================================
    # URL VALIDATION
    # =========================================================

    def _is_http_url(
        self,
        url
    ):

        try:

            parsed = urlparse(
                url
            )

            return parsed.scheme.lower() in {
                "http",
                "https",
            }

        except ValueError:

            return False

    # =========================================================
    # LAST RESULT
    # =========================================================

    def get_last_result(self):

        return self.last_result

    # =========================================================
    # LAST URL
    # =========================================================

    def get_last_url(self):

        return self.last_url

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        connected = False

        if self.enabled:

            connected = (
                self.check_connection()
            )

        return {
            "enabled":
                self.enabled,

            "status":
                self.status_state,

            "internet":
                connected,

            "last_url":
                self.last_url,
        }
