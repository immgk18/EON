"""
EON API
=======
Secure API and web interface backend for EON.
"""

import os
import secrets

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from core.eon import EON


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="EON API",
    version="1.0",
    description="Executive Orchestration Network"
)


# ============================================================
# EON CORE
# ============================================================

eon = EON()


# ============================================================
# SECURITY
# ============================================================

API_TOKEN = os.getenv("EON_API_TOKEN", "").strip()


def verify_token(
    x_eon_token: str | None = Header(default=None)
):
    """
    Verify the EON API token.
    """

    if not API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="EON_API_TOKEN is not configured on the server."
        )

    if not x_eon_token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    if not secrets.compare_digest(
        x_eon_token.strip(),
        API_TOKEN
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid EON API token."
        )

    return True


# ============================================================
# REQUEST MODEL
# ============================================================

class CommandRequest(BaseModel):
    command: str


# ============================================================
# BASIC API
# ============================================================

@app.get("/api")
def api_home():
    return {
        "success": True,
        "name": "EON API",
        "status": "ONLINE",
        "version": "1.0",
        "authentication": "TOKEN_REQUIRED"
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "status": "ONLINE"
    }


# ============================================================
# STATUS
# ============================================================

@app.get("/api/status")
def get_status(
    x_eon_token: str | None = Header(default=None)
):
    verify_token(x_eon_token)

    try:
        status = eon.status()
    except Exception as error:
        status = {
            "status": "ONLINE",
            "error": str(error)
        }

    return {
        "success": True,
        "eon": status
    }


# ============================================================
# COMMAND
# ============================================================

@app.post("/api/command")
def execute_command(
    request: CommandRequest,
    x_eon_token: str | None = Header(default=None)
):
    verify_token(x_eon_token)

    command = request.command.strip()

    if not command:
        raise HTTPException(
            status_code=400,
            detail="Command cannot be empty."
        )

    if len(command) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Command is too long."
        )

    try:
        response = eon.handle_command(command)

        return {
            "success": True,
            "command": command,
            "response": str(response)
        }

    except Exception as error:
        return {
            "success": False,
            "command": command,
            "response": f"EON encountered an error: {error}"
        }


# ============================================================
# WEB INTERFACE
# ============================================================

@app.get("/", response_class=HTMLResponse)
def interface():
    """
    The main EON interface.
    """

    try:
        with open("index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(
                content=file.read(),
                status_code=200
            )

    except FileNotFoundError:
        return HTMLResponse(
            content="""
            <html>
                <body style="background:#000;color:#ffd84d;
                font-family:Arial;text-align:center;padding-top:20%;">
                    <h1>EON</h1>
                    <p>index.html not found.</p>
                </body>
            </html>
            """,
            status_code=404
        )
