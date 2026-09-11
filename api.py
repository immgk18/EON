"""
EON
===
Executive Orchestration Network

EON Web API
"""

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from core.eon import EON


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INDEX_FILE = BASE_DIR / "index.html"

HOST = os.getenv(
    "EON_API_HOST",
    "0.0.0.0"
)

PORT = int(
    os.getenv(
        "PORT",
        "5000"
    )
)


# ============================================================
# REQUEST MODEL
# ============================================================

class CommandRequest(BaseModel):
    command: str


# ============================================================
# EON API
# ============================================================

class EONAPI:
    """
    Main EON API controller.
    """

    def __init__(self):

        self.eon = EON()

        self.app = FastAPI(
            title="EON",
            description=(
                "Executive Orchestration Network"
            ),
            version="4.0",
        )

        self._register_routes()


    # ========================================================
    # ROUTES
    # ========================================================

    def _register_routes(self):

        # ----------------------------------------------------
        # EON INTERFACE
        # ----------------------------------------------------

        @self.app.get("/")
        async def home():

            if not INDEX_FILE.exists():

                raise HTTPException(
                    status_code=404,
                    detail=(
                        "index.html was not found."
                    )
                )

            return FileResponse(
                INDEX_FILE,
                media_type="text/html"
            )


        # ----------------------------------------------------
        # HEALTH CHECK
        # ----------------------------------------------------

        @self.app.get("/health")
        async def health():

            return {
                "success": True,
                "status": "ONLINE",
                "system": "EON"
            }


        # ----------------------------------------------------
        # API INFORMATION
        # ----------------------------------------------------

        @self.app.get("/api")
        async def api_info():

            return {
                "success": True,
                "name": "EON",
                "system": (
                    "Executive Orchestration Network"
                ),
                "version": "4.0",
                "status": "ONLINE",
                "authentication": "DISABLED"
            }


        # ----------------------------------------------------
        # EON STATUS
        # ----------------------------------------------------

        @self.app.get("/api/status")
        async def status():

            try:

                result = self.eon.status()

                return {
                    "success": True,
                    "status": result
                }

            except Exception as error:

                return {
                    "success": False,
                    "error": str(error)
                }


        # ----------------------------------------------------
        # EON COMMAND
        # ----------------------------------------------------

        @self.app.post("/api/command")
        async def command(
            request: CommandRequest
        ):

            command_text = (
                request.command.strip()
            )


            if not command_text:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Command cannot be empty."
                    )
                )


            if len(command_text) > 2000:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Command is too long."
                    )
                )


            try:

                result = self.eon.handle_command(
                    command_text
                )


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


        # ----------------------------------------------------
        # AVAILABLE MODULES
        # ----------------------------------------------------

        @self.app.get("/api/modules")
        async def modules():

            try:

                available_modules = (
                    self.eon.router
                    .get_available_modules()
                )


                return {
                    "success": True,
                    "modules": available_modules
                }


            except Exception as error:

                return {
                    "success": False,
                    "error": str(error)
                }


        # ----------------------------------------------------
        # RESET SESSION
        # ----------------------------------------------------

        @self.app.post("/api/reset")
        async def reset():

            try:

                self.eon.context.clear()


                return {
                    "success": True,
                    "message": (
                        "EON session reset."
                    )
                }


            except Exception as error:

                return {
                    "success": False,
                    "error": str(error)
                }


    # ========================================================
    # SERVER
    # ========================================================

    def run(self):

        uvicorn.run(
            self.app,
            host=HOST,
            port=PORT
        )


# ============================================================
# GLOBAL API INSTANCE
# ============================================================

eon_api = EONAPI()

app = eon_api.app


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    eon_api.run()
