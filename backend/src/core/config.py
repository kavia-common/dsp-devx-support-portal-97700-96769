"""
Application configuration module.

Loads environment-driven settings for app metadata, CORS, and logging.
Use .env to configure:
- APP_NAME: Overrides the FastAPI title.
- ALLOW_ORIGINS: Comma-separated origins for CORS (default: http://localhost:3000).
- LOG_LEVEL: Logging level name (e.g., INFO, DEBUG, WARNING). Default: INFO.
"""
from __future__ import annotations

import logging
import os
from typing import List

from dotenv import load_dotenv

# Load environment variables from .env if present (non-fatal if missing)
load_dotenv()


def _parse_origins(value: str) -> List[str]:
    # Split by comma and strip spaces; ignore empty entries
    return [v.strip() for v in value.split(",") if v.strip()]


# PUBLIC_INTERFACE
def get_settings() -> dict:
    """Get application settings resolved from environment variables.
    
    Returns a dict with:
    - app_name: str
    - allow_origins: List[str]
    - log_level: int (logging level)
    """
    app_name = os.getenv("APP_NAME", "DSP DevX Support Backend")
    allow_origins_raw = os.getenv("ALLOW_ORIGINS", "http://localhost:3000")
    allow_origins = _parse_origins(allow_origins_raw) if allow_origins_raw else ["http://localhost:3000"]
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    return {
        "app_name": app_name,
        "allow_origins": allow_origins,
        "log_level": log_level,
    }
