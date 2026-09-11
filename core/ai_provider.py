"""
EON AI Provider
===============
Provider abstraction for EON's artificial intelligence layer.

EON can use different AI backends without changing the Brain.

Current provider:
- Local Ollama-compatible API

Future providers can be added later.
"""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class AIProvider:
    """Base interface for EON AI providers."""

    def __init__(
        self,
        name="unknown",
        model=""
    ):
        self.name = name
        self.model = model
        self.connected = False
        self.last_response = None
        self.last_error = None

    def connect(self):
        """Check whether the provider is available."""
        return False

    def generate(
        self,
        prompt,
        temperature=0.7,
        max_tokens=2048
    ):
        """Generate an AI response."""
        raise NotImplementedError

    def status(self):
        return {
            "provider": self.name,
            "model": self.model,
            "connected": self.connected,
            "status": (
                "ONLINE"
                if self.connected
                else "OFFLINE"
            ),
        }


class LocalOllamaProvider(AIProvider):
    """
    Local AI provider using an Ollama-compatible API.

    Default endpoint:
    http://127.0.0.1:11434
    """

    def __init__(
        self,
        model="",
        host="http://127.0.0.1:11434"
    ):

        super().__init__(
            name="local",
            model=model
        )

        self.host = host.rstrip("/")

        self.generate_endpoint = (
            f"{self.host}/api/generate"
        )

        self.tags_endpoint = (
            f"{self.host}/api/tags"
        )

    # =========================================================
    # CONNECTION
    # =========================================================

    def connect(self):

        try:

            request = Request(
                self.tags_endpoint,
                method="GET"
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                response.read()

            self.connected = True
            self.last_error = None

            return True

        except (
            URLError,
            HTTPError,
            TimeoutError,
            OSError
        ) as error:

            self.connected = False
            self.last_error = str(error)

            return False

    # =========================================================
    # AVAILABLE MODELS
    # =========================================================

    def get_models(self):

        try:

            request = Request(
                self.tags_endpoint,
                method="GET"
            )

            with urlopen(
                request,
                timeout=5
            ) as response:

                data = response.read()

            result = json.loads(
                data.decode("utf-8")
            )

            models = []

            for item in result.get(
                "models",
                []
            ):

                name = item.get(
                    "name"
                )

                if name:
                    models.append(name)

            return models

        except (
            URLError,
            HTTPError,
            TimeoutError,
            OSError,
            json.JSONDecodeError
        ):

            return []

    # =========================================================
    # MODEL SELECTION
    # =========================================================

    def set_model(
        self,
        model
    ):

        if not model:

            return False

        self.model = model.strip()

        return True

    # =========================================================
    # GENERATION
    # =========================================================

    def generate(
        self,
        prompt,
        temperature=0.7,
        max_tokens=2048
    ):

        if not prompt:

            return None

        if not self.model:

            self.last_error = (
                "No AI model configured."
            )

            return None

        payload = {

            "model":
                self.model,

            "prompt":
                prompt,

            "stream":
                False,

            "options": {

                "temperature":
                    temperature,

                "num_predict":
                    max_tokens,
            },
        }

        try:

            request = Request(

                self.generate_endpoint,

                data=json.dumps(
                    payload
                ).encode("utf-8"),

                headers={
                    "Content-Type":
                        "application/json"
                },

                method="POST",
            )

            with urlopen(
                request,
                timeout=120
            ) as response:

                data = response.read()

            result = json.loads(
                data.decode("utf-8")
            )

            answer = (
                result
                .get("response", "")
                .strip()
            )

            if answer:

                self.connected = True
                self.last_response = answer
                self.last_error = None

                return answer

            self.last_error = (
                "AI returned an empty response."
            )

            return None

        except (
            URLError,
            HTTPError,
            TimeoutError,
            OSError,
            json.JSONDecodeError
        ) as error:

            self.connected = False
            self.last_error = str(error)

            return None

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        result = super().status()

        result.update({

            "host":
                self.host,

            "available_models":
                self.get_models(),

            "last_error":
                self.last_error,
        })

        return result


class AIProviderManager:
    """Manages EON's active AI provider."""

    def __init__(
        self,
        provider="local",
        model=""
    ):

        self.providers = {}

        self.active_provider = None

        self.register_provider(
            "local",
            LocalOllamaProvider(
                model=model
            )
        )

        self.set_provider(
            provider
        )

    # =========================================================
    # REGISTER
    # =========================================================

    def register_provider(
        self,
        name,
        provider
    ):

        if not name:
            return False

        if provider is None:
            return False

        self.providers[
            name.lower()
        ] = provider

        return True

    # =========================================================
    # SET PROVIDER
    # =========================================================

    def set_provider(
        self,
        name
    ):

        if not name:
            return False

        name = name.lower().strip()

        provider = self.providers.get(
            name
        )

        if provider is None:
            return False

        self.active_provider = provider

        return True

    # =========================================================
    # GET PROVIDER
    # =========================================================

    def get_provider(self):

        return self.active_provider

    # =========================================================
    # CONNECT
    # =========================================================

    def connect(self):

        if self.active_provider is None:

            return False

        return self.active_provider.connect()

    # =========================================================
    # GENERATE
    # =========================================================

    def generate(
        self,
        prompt,
        temperature=0.7,
        max_tokens=2048
    ):

        if self.active_provider is None:

            return None

        return self.active_provider.generate(
            prompt,
            temperature,
            max_tokens
        )

    # =========================================================
    # MODELS
    # =========================================================

    def get_models(self):

        if isinstance(
            self.active_provider,
            LocalOllamaProvider
        ):

            return (
                self.active_provider
                .get_models()
            )

        return []

    # =========================================================
    # STATUS
    # =========================================================

    def status(self):

        if self.active_provider is None:

            return {
                "provider": None,
                "status": "NO_PROVIDER",
            }

        return self.active_provider.status()
