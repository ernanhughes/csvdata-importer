"""Class wrapper around a configuration file."""
from typing import Any, Dict


class Config(Dict[str, Any]):
    """Class wrapper around a configuration file."""

    def __init__(self, config: str) -> None:
        """Initialize the config."""
        self.config = config


    def __str__(self) -> str:
        """Return the config as a string."""
        return self.config

