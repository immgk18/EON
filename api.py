"""
EON API
=======
Web API and browser interface for EON.
"""

import os
import secrets

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.eon import EON


# ============================================================
# REQUEST MODEL
# ============================================================

class CommandRequest(BaseModel):
    command: str


# ============================================================
# EON API
# ============================================================

class EONAPI:

    def __init__(self):
        self.eon = EON()

        self.app = FastAPI(
            title="EON API",
            version="1.0",
            description="Executive Orchestration Network API"
        )

        self.api_token = os.getenv("EON_API_TOKEN", "")

        self._register_routes()

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------

    def authenticate(self, token):
        if not self.api_token:
            return False

        if not token:
            return False

        return secrets.compare_digest(
            str(token),
            str(self.api_token)
        )

    def require_auth(self, token):
        if not self.api_token:
            raise HTTPException(
                status_code=503,
                detail="EON API token is not configured on the server."
            )

        if not self.authenticate(token):
            raise HTTPException(
                status_code=401,
                detail="Invalid EON API token."
            )

    # --------------------------------------------------------
    # ROUTES
    # --------------------------------------------------------

    def _register_routes(self):

        @self.app.get("/")
        async def home():
            return {
                "name": "EON API",
                "system": "Executive Orchestration Network",
                "version": "1.0",
                "status": "ONLINE",
                "success": True,
                "authentication": (
                    "CONFIGURED"
                    if self.api_token
                    else "TOKEN_REQUIRED"
                )
            }

        @self.app.get("/health")
        async def health():
            return {
                "status": "ONLINE",
                "success": True
            }

        @self.app.get("/api")
        async def api_info():
            return {
                "name": "EON API",
                "status": "ONLINE",
                "version": "1.0",
                "success": True
            }

        @self.app.get("/api/status")
        async def status(
            x_eon_token: str | None = Header(default=None)
        ):
            self.require_auth(x_eon_token)

            try:
                return {
                    "success": True,
                    "status": self.eon.status()
                }
            except Exception as error:
                return {
                    "success": False,
                    "error": str(error)
                }

        @self.app.post("/api/command")
        async def command(
            request: CommandRequest,
            x_eon_token: str | None = Header(default=None)
        ):
            self.require_auth(x_eon_token)

            command_text = request.command.strip()

            if not command_text:
                raise HTTPException(
                    status_code=400,
                    detail="Command cannot be empty."
                )

            if len(command_text) > 2000:
                raise HTTPException(
                    status_code=400,
                    detail="Command is too long."
                )

            try:
                result = self.eon.handle_command(command_text)

                return {
                    "success": True,
                    "command": command_text,
                    "response": result
                }

            except Exception as error:
                return {
                    "success": False,
                    "error": str(error)
                }

        @self.app.get("/api/modules")
        async def modules(
            x_eon_token: str | None = Header(default=None)
        ):
            self.require_auth(x_eon_token)

            try:
                return {
                    "success": True,
                    "modules": self.eon.router.get_available_modules()
                }
            except Exception as error:
                return {
                    "success": False,
                    "error": str(error)
                }

        @self.app.get("/app", response_class=HTMLResponse)
        async def app():
            return self._html()

    # --------------------------------------------------------
    # WEB INTERFACE
    # --------------------------------------------------------

    def _html(self):

        return r"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0"
>

<title>EON</title>

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #000;
    color: #ffd84d;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    display: flex;
    align-items: center;
    justify-content: center;
}

/* --------------------------------------------------
   BACKGROUND
-------------------------------------------------- */

.background {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(
            circle at center,
            rgba(255, 210, 50, 0.08),
            transparent 32%
        ),
        #000;
}

/* --------------------------------------------------
   MAIN
-------------------------------------------------- */

.container {
    position: relative;
    z-index: 2;

    width: min(1100px, 94vw);
    height: 100vh;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 30px;
}

/* --------------------------------------------------
   TITLE
-------------------------------------------------- */

.title {
    position: absolute;
    top: 35px;

    text-align: center;

    letter-spacing: 18px;

    font-size: clamp(32px, 5vw, 58px);

    font-weight: 300;

    text-shadow:
        0 0 10px #ffd84d,
        0 0 30px rgba(255, 210, 50, 0.7);

    animation: titlePulse 3s infinite ease-in-out;
}

@keyframes titlePulse {

    0%,
    100% {
        opacity: 0.8;
    }

    50% {
        opacity: 1;
    }
}

/* --------------------------------------------------
   SUBTITLE
-------------------------------------------------- */

.subtitle {

    position: absolute;

    top: 105px;

    font-size: 12px;

    letter-spacing: 7px;

    opacity: 0.55;
}

/* --------------------------------------------------
   CORE
-------------------------------------------------- */

.core {

    position: relative;

    width: min(500px, 75vw);
    height: min(500px, 75vw);

    display: flex;

    align-items: center;
    justify-content: center;

    --core-color: #ffd21c;

    transition:
        --core-color 0.4s ease;
}

/* OUTER ENERGY */

.energy {
    position: absolute;

    width: 100%;
    height: 100%;

    border-radius: 50%;

    border: 1px solid var(--core-color);

    opacity: 0.35;

    box-shadow:
        0 0 20px var(--core-color),
        inset 0 0 30px var(--core-color);

    animation:
        rotate 18s linear infinite,
        breathe 3s ease-in-out infinite;
}

/* SECOND RING */

.energy::before {

    content: "";

    position: absolute;

    inset: 8%;

    border-radius: 50%;

    border: 1px dashed var(--core-color);

    opacity: 0.5;

    animation: rotateReverse 12s linear infinite;
}

/* THIRD RING */

.energy::after {

    content: "";

    position: absolute;

    inset: 18%;

    border-radius: 50%;

    border: 1px solid var(--core-color);

    opacity: 0.3;

    animation: rotate 8s linear infinite;
}

/* --------------------------------------------------
   HOLLOW CORE
-------------------------------------------------- */

.hollow {

    position: relative;

    width: 72%;
    height: 72%;

    border-radius: 50%;

    background:

        radial-gradient(
            circle,
            #000 0%,
            #000 48%,
            rgba(0,0,0,0.95) 62%,
            transparent 75%
        );

    border: 2px solid var(--core-color);

    box-shadow:

        0 0 15px var(--core-color),

        0 0 40px var(--core-color),

        inset 0 0 35px var(--core-color),

        inset 0 0 90px rgba(0,0,0,1);

    animation:
        corePulse 2.5s infinite ease-in-out;
}

/* LIVING ENERGY */

.hollow::before {

    content: "";

    position: absolute;

    inset: 5%;

    border-radius: 50%;

    border: 2px solid var(--core-color);

    opacity: 0.45;

    filter: blur(1px);

    animation:
        spin 5s linear infinite;
}

.hollow::after {

    content: "";

    position: absolute;

    inset: 20%;

    border-radius: 50%;

    border: 1px dashed var(--core-color);

    opacity: 0.6;

    animation:
        spinReverse 4s linear infinite;
}

/* --------------------------------------------------
   BURST
-------------------------------------------------- */

.burst {

    position: absolute;

    width: 10px;
    height: 10px;

    border-radius: 50%;

    background: var(--core-color);

    box-shadow:
        0 0 20px var(--core-color),
        0 0 50px var(--core-color),
        0 0 100px var(--core-color);

    opacity: 0;

    pointer-events: none;
}

.burst.active {

    animation: burst 0.9s ease-out;
}

@keyframes burst {

    0% {
        transform: scale(1);
        opacity: 1;
    }

    100% {
        transform: scale(35);
        opacity: 0;
    }
}

/* --------------------------------------------------
   STATUS
-------------------------------------------------- */

.status {

    position: absolute;

    bottom: 135px;

    font-size: 12px;

    letter-spacing: 5px;

    text-transform: uppercase;

    opacity: 0.7;
}

/* --------------------------------------------------
   COMMAND
-------------------------------------------------- */

.command-box {

    position: absolute;

    bottom: 55px;

    width: min(720px, 88vw);

    display: flex;

    gap: 10px;
}

.command-box input {

    flex: 1;

    padding: 17px 22px;

    border-radius: 30px;

    border: 1px solid #ffd84d;

    outline: none;

    background: rgba(0,0,0,0.7);

    color: #ffd84d;

    font-size: 15px;

    box-shadow:
        0 0 15px rgba(255,210,30,0.25);

}

.command-box button {

    width: 58px;

    border-radius: 50%;

    border: 1px solid #ffd84d;

    background: #050505;

    color: #ffd84d;

    cursor: pointer;

    font-size: 20px;

    box-shadow:
        0 0 15px rgba(255,210,30,0.35);

}

.command-box button:hover {

    background: #ffd84d;

    color: #000;

}

/* --------------------------------------------------
   RED MODE
-------------------------------------------------- */

body.unlimited {

    --core-color: #ff2525;
}

body.unlimited .core {

    --core-color: #ff2525;
}

body.unlimited .title {

    color: #ff2525;

    text-shadow:
        0 0 10px #ff2525,
        0 0 35px rgba(255,0,0,0.8);
}

body.unlimited .status {

    color: #ff2525;
}

/* --------------------------------------------------
   ANIMATIONS
-------------------------------------------------- */

@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes rotateReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}

@keyframes spin {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

@keyframes spinReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}

@keyframes breathe {

    0%,
    100% {
        transform: scale(0.98);
    }

    50% {
        transform: scale(1.04);
    }
}

@keyframes corePulse {

    0%,
    100% {
        transform: scale(0.98);
    }

    50% {
        transform: scale(1.03);
    }
}

/* --------------------------------------------------
   MOBILE
-------------------------------------------------- */

@media (max-width: 600px) {

    .title {
        letter-spacing: 10px;
    }

    .subtitle {
        font-size: 8px;
        letter-spacing: 4px;
    }

    .status {
        bottom: 120px;
    }

}

</style>

</head>

<body>

<div class="background"></div>

<div class="container">

    <div class="title">
        EON
    </div>

    <div class="subtitle">
        THINK · ANALYZE · EXECUTE
    </div>

    <div class="core">

        <div class="energy"></div>

        <div class="hollow"></div>

        <div
            id="burst"
            class="burst"
        ></div>

    </div>

    <div
        id="status"
        class="status"
    >
        SYSTEM ONLINE
    </div>

    <div class="command-box">

        <input
            id="command"
            type="text"
            placeholder="Speak to EON..."
        >

        <button
            onclick="sendCommand()"
        >
            ➤
        </button>

    </div>

</div>

<script>

let token = localStorage.getItem("eon_token") || "";

if (!token) {

    token = prompt(
        "Enter your EON API token:"
    );

    if (token) {
        localStorage.setItem(
            "eon_token",
            token
        );
    }
}

const commandInput =
    document.getElementById("command");

const status =
    document.getElementById("status");

const burst =
    document.getElementById("burst");


function triggerBurst() {

    burst.classList.remove("active");

    void burst.offsetWidth;

    burst.classList.add("active");
}


function setUnlimited(enabled) {

    triggerBurst();

    document.body.classList.toggle(
        "unlimited",
        enabled
    );

    status.textContent =
        enabled
        ? "LIMITS RELEASED"
        : "SYSTEM ONLINE";
}


function speak(text) {

    if (!text) return;

    if ("speechSynthesis" in window) {

        window.speechSynthesis.cancel();

        const speech =
            new SpeechSynthesisUtterance(text);

        speech.rate = 1;
        speech.pitch = 0.9;
        speech.volume = 1;

        window.speechSynthesis.speak(
            speech
        );
    }
}


async function sendCommand() {

    const command =
        commandInput.value.trim();

    if (!command) return;

    status.textContent =
        "THINKING...";

    try {

        const response =
            await fetch("/api/command", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json",

                    "X-EON-TOKEN":
                        token
                },

                body: JSON.stringify({
                    command: command
                })

            });

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Connection failed."
            );
        }

        const answer =
            typeof data.response === "string"
            ? data.response
            : JSON.stringify(
                data.response
            );

        const lower =
            command.toLowerCase();

        if (
            lower.includes(
                "eon has no limits"
            )
        ) {

            setUnlimited(true);

        }

        if (
            lower.includes(
                "eon has limits"
            )
        ) {

            setUnlimited(false);

        }

        status.textContent =
            answer || "READY";

        speak(answer);

        commandInput.value = "";

    } catch (error) {

        status.textContent =
            "CONNECTION ERROR";

        console.error(error);

    }

}


commandInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendCommand();
        }

    }
);

</script>

</body>

</html>
"""

    # --------------------------------------------------------
    # RUN SERVER
    # --------------------------------------------------------

    def run(self):

        host = os.getenv(
            "EON_API_HOST",
            "0.0.0.0"
        )

        port = int(
            os.getenv(
                "PORT",
                "5000"
            )
        )

        uvicorn.run(
            self.app,
            host=host,
            port=port
        )


# ============================================================
# LOCAL ENTRY POINT
# ============================================================

if __name__ == "__main__":

    server = EONAPI()
    server.run()
