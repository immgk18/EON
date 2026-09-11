"""
EON AI Provider
===============
Provider abstraction for EON's AI layer.

Supports:
- Text generation
- Vision generation
- Local Ollama-compatible models

Future providers can be added without changing
the EON Brain or Vision modules.
"""

import base64
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
        return False

    def generate(
        self,
        prompt,
        temperature=0.7,
        max_tokens=2048
    ):
        raise NotImplementedError

    def generate_vision(
        self,
        prompt,
        image_base64,
        temperature=0.7,
        max_tokens=2048
    ):
        raise NotImplementedError

    def status(self):

        return {
            "provider":
                self.name,

            "model":
                self.model,

            "connected":
                self.connected,

            "status":
                (
                    "ONLINE"
                    if self.connected
                    else "OFFLINE"
                ),

            "last_error":
                self.last_error,
        }


class LocalOllamaProvider(AIProvider):
    """
    Local AI provider using Ollama's API.

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
    # SET MODEL
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
    # TEXT GENERATION
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

            result = self._post(
                self.generate_endpoint,
                payload
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

        except Exception as error:

            self.connected = False
            self.last_error = str(error)

            return None

    # =========================================================
    # VISION GENERATION
    # =========================================================

    def generate_vision(
        self,
        prompt,
        image_base64,
        temperature=0.7,
        max_tokens=2048
    ):
        """
        Send an image and prompt to a vision-capable
        Ollama model.

        image_base64 must contain the raw Base64
        representation of the image.
        """

        if not prompt:

            prompt = (
                "Analyze this image and describe "
                "the important information you can see."
            )

        if not image_base64:

            self.last_error = (
                "No image data supplied."
            )

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

            "images": [
                image_base64
            ],

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

            result = self._post(
                self.generate_endpoint,
                payload
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
                "Vision model returned "
                "an empty response."
            )

            return None

        except Exception as error:

            self.connected = False
            self.last_error = str(error)

            return None

    # =========================================================
    # HTTP POST
    # =========================================================

    def _post(
        self,
        url,
        payload
    ):

        request = Request(

            url,

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

        return json.loads(
            data.decode("utf-8")
        )

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

        if not name or provider is None:
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
    # TEXT GENERATION
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
    # VISION GENERATION
    # =========================================================

    def generate_vision(
        self,
        prompt,
        image_base64,
        temperature=0.7,
        max_tokens=2048
    ):

        if self.active_provider is None:
            return None

        return self.active_provider.generate_vision(
            prompt,
            image_base64,
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
