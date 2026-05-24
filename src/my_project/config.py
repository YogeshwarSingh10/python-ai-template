import logging
import os
from datetime import datetime

import yaml
from dotenv import load_dotenv

load_dotenv()


# ── Logging ───────────────────────────────────────────────────────────────────

class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG:    "\033[90m",
        logging.INFO:     "\033[35m",
        logging.WARNING:  "\033[93m",
        logging.ERROR:    "\033[91m",
        logging.CRITICAL: "\033[1;91m",
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        levelname = f"{color}{record.levelname}{self.RESET}"
        filename = os.path.basename(record.pathname)
        location = f"{color}{filename}:{record.lineno}{self.RESET}"
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        message = record.getMessage()
        if record.exc_info:
            exception_text = self.formatException(record.exc_info)
            message = f"{message}\n{exception_text}"
        return f"[{levelname}] {timestamp} | {location} | {message}"


def setup_logging(level: int = logging.INFO) -> None:
    """Call once at the top of main.py before anything else."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return
    root_logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter())
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Use in every module: logger = get_logger(__name__)"""
    return logging.getLogger(name)


# ── Config ────────────────────────────────────────────────────────────────────

def _load_yaml(path: str = "config.yaml") -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"config.yaml not found at: {path}")
    with open(path) as f:
        return yaml.safe_load(f) or {}

cfg: dict = _load_yaml()


# ── Secrets (from .env) ───────────────────────────────────────────────────────

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


OPENROUTER_API_KEY: str = get_env("OPENROUTER_API_KEY")


# ── Non-secret config (from config.yaml) ─────────────────────────────────────

OPENROUTER_BASE_URL: str = cfg["llm"]["base_url"]
DEFAULT_MODEL: str = cfg["llm"]["default_model"]
