import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


# ── Logging ───────────────────────────────────────────────────────────────────


class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    COLORS = {
        logging.DEBUG: "\033[90m",
        logging.INFO: "\033[35m",
        logging.WARNING: "\033[93m",
        logging.ERROR: "\033[91m",
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


# ── YAML settings source ──────────────────────────────────────────────────────

_CONFIG_YAML = Path(__file__).parent.parent.parent / "config.yaml"


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """Loads non-secret config from config.yaml at the project root."""

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[None, str, bool]:
        return None, field_name, False  # handled by __call__

    def __call__(self) -> dict[str, Any]:  # type: ignore[override]  # yaml.safe_load stubs return Any; signature forced by PydanticBaseSettingsSource ABC
        if not _CONFIG_YAML.exists():
            raise FileNotFoundError(f"config.yaml not found at: {_CONFIG_YAML}")
        with _CONFIG_YAML.open() as f:
            return yaml.safe_load(f) or {}


# ── Settings models ───────────────────────────────────────────────────────────


class LLMSettings(BaseModel):
    base_url: str
    default_model: str
    temperature: float = Field(ge=0.0, le=2.0)
    max_tokens: int = Field(gt=0)


class Settings(BaseSettings):
    """
    Single source of truth for all configuration.

    Secrets  → .env / environment variables  (e.g. OPENROUTER_API_KEY)
    Non-secrets → config.yaml                (e.g. llm.default_model)

    Override any config.yaml value at runtime via env var:
        LLM__DEFAULT_MODEL=openai/gpt-4o pytest
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    # Secrets (from .env / env vars only)
    openrouter_api_key: str

    # Non-secrets (from config.yaml, overridable via env vars)
    llm: LLMSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        **kwargs: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            kwargs["env_settings"],
            kwargs["dotenv_settings"],
            YamlConfigSettingsSource(settings_cls),
            kwargs["init_settings"],
        )


settings = Settings()  # type: ignore[call-arg]  # fields are populated from env/yaml sources
