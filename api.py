"""
EON
===
Executive Orchestration Network

Web API + EON browser interface.
"""

import os
import secrets
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from core.eon import EON


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "index.html"

API_TOKEN = os.getenv("EON_API_TOKEN", "").strip()

HOST = os.getenv("EON_API_HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))


# ============================================================
# REQUEST MODEL
# ============================================================

class CommandRequest(BaseModel):
    command: str


# ============================================================
# EON INSTANCE
# ============================================================

eon = EON()


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="EON",
    description="Executive Orchestration Network",
    version="4.0",
)


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate(token: str | None) -> bool:
    """
    Verify the EON API token.

    The server token must be configured through
    EON_API_TOKEN.
    """

    if not API_TOKEN:
        return False

    if not token:
        return False

    return secrets.compare_digest(
        str(token),
        str(API_TOKEN),
    )


def require_auth(token: str | None):
    """
    Protect EON control endpoints.
    """

    if not API_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="EON API token is not configured.",
        )

    if not authenticate(token):
        raise HTTPException(
            status_code=401,
            detail="Invalid EON API token.",
        )


# ============================================================
# ROOT
# ============================================================

@app.get("/")
async def home():
    """
    Serve the EON interface.
    """

    if not INDEX_FILE.exists():
        return {
            "name": "EON",
            "status": "ONLINE",
            "error": "index.html not found.",
        }

    return FileResponse(
        INDEX_FILE,
        media_type="text/html",
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
async def health():
    return {
        "success": True,
        "status": "ONLINE",
        "system": "EON",
    }


# ============================================================
# API INFORMATION
# ============================================================

@app.get("/api")
async def api_info():
    return {
        "success": True,
        "name": "EON",
        "system": "Executive Orchestration Network",
        "version": "4.0",
        "status": "ONLINE",
        "authentication": (
            "CONFIGURED"
            if API_TOKEN
            else "NOT_CONFIGURED"
        ),
    }


# ============================================================
# STATUS
# ============================================================

@app.get("/api/status")
async def status(
    x_eon_token: str | None = Header(default=None),
):
    require_auth(x_eon_token)

    try:
        return {
            "success": True,
            "status": eon.status(),
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# COMMAND
# ============================================================

@app.post("/api/command")
async def command(
    request: CommandRequest,
    x_eon_token: str | None = Header(default=None),
):
    require_auth(x_eon_token)

    command_text = request.command.strip()

    if not command_text:
        raise HTTPException(
            status_code=400,
            detail="Command cannot be empty.",
        )

    if len(command_text) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Command is too long.",
        )

    try:
        result = eon.handle_command(command_text)

        return {
            "success": True,
            "command": command_text,
            "response": result,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# MODULES
# ============================================================

@app.get("/api/modules")
async def modules(
    x_eon_token: str | None = Header(default=None),
):
    require_auth(x_eon_token)

    try:
        return {
            "success": True,
            "modules": eon.router.get_available_modules(),
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# RESET
# ============================================================

@app.post("/api/reset")
async def reset(
    x_eon_token: str | None = Header(default=None),
):
    require_auth(x_eon_token)

    try:
        eon.context.clear()

        return {
            "success": True,
            "message": "EON session reset.",
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )
