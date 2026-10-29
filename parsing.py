"""Configuration loading with safe defaults and JSON comment support."""
from __future__ import annotations

import json
import re
from typing import Any


class Config:
    """Read and validate the game configuration.

    The maze is drawn inside a fixed 1600x900 gameplay frame. These limits
    match the maximum grid that fits that frame at the normal cell size.
    Requests larger than the frame are clamped rather than overflowing it.
    """
    MAX_MAZE_WIDTH = 29
    MAX_MAZE_HEIGHT = 17

    DEFAULT_CONFIG: dict[str, Any] = {
        "highscore_filename": "highscores.json",
        "lives": 3,
        "pacgum": 42,
        "points_per_pacgum": 10,
        "points_per_super_pacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90,
        "levels": [{"width": 15, "height": 15} for _ in range(10)],
    }

    def __init__(self, filename: str = "config.json") -> None:
        self.filename = filename

    @staticmethod
    def _remove_comments(content: str) -> str:
        """Remove # and // comments without removing markers inside strings."""
        result: list[str] = []
        in_string = False
        escaped = False
        i = 0
        while i < len(content):
            char = content[i]
            if in_string:
                result.append(char)
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                i += 1
                continue
            if char == '"':
                in_string = True
                result.append(char)
                i += 1
            elif char == "#":
                while i < len(content) and content[i] != "\n":
                    i += 1
            elif content.startswith("//", i):
                while i < len(content) and content[i] != "\n":
                    i += 1
            else:
                result.append(char)
                i += 1
        return "".join(result)

    def load_config(self, filename: str | None = None) -> dict[str, Any]:
        """Load a JSON object after stripping supported comments."""
        path = filename or self.filename
        with open(path, "r", encoding="utf-8") as file:
            parsed = json.loads(self._remove_comments(file.read()))
        if not isinstance(parsed, dict):
            raise ValueError("configuration root must be an object")
        return parsed

    @staticmethod
    def _positive_int(value: Any, minimum: int = 1) -> bool:
        return isinstance(value, int) and not isinstance(value, bool) and value >= minimum

    def check_height_width(self, width: int, height: int) -> tuple[str, bool]:
        """Check that dimensions are usable by the maze generator."""
        if width < 7:
            return "width", False
        if height < 7:
            return "height", False
        return "", True

    def check_config(self, filename: str | None = None) -> dict[str, Any]:
        """Validate values individually, falling back to safe defaults."""
        defaults = self.DEFAULT_CONFIG
        try:
            raw = self.load_config(filename)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            print(f"Warning: cannot read configuration ({error}); using defaults.")
            return {**defaults, "levels": [dict(x) for x in defaults["levels"]]}

        config: dict[str, Any] = {}
        for key, default in defaults.items():
            value = raw.get(key, default)
            if key == "highscore_filename":
                valid = isinstance(value, str) and value.strip().endswith(".json")
                config[key] = value.strip() if valid else default
            elif key == "levels":
                levels: list[dict[str, int]] = []
                if isinstance(value, list):
                    for item in value[:50]:
                        width = item.get("width", 15) if isinstance(item, dict) else 15
                        height = item.get("height", 15) if isinstance(item, dict) else 15
                        if not self._positive_int(width, 7):
                            width = 15
                        if not self._positive_int(height, 7):
                            height = 15
                        # Never let config dimensions exceed the visible maze frame.
                        # Clamp each axis independently: e.g. 100x100 becomes 29x17.
                        width = min(width, self.MAX_MAZE_WIDTH)
                        height = min(height, self.MAX_MAZE_HEIGHT)
                        levels.append({"width": width, "height": height})
                if not levels:
                    levels = [dict(x) for x in defaults["levels"]]
                # A non-empty configured list defines the campaign length.
                config[key] = levels
            elif key in ("lives", "level_max_time"):
                config[key] = value if self._positive_int(value) else default
            else:
                config[key] = value if self._positive_int(value, 0) else default
            if key in raw and config[key] == default and raw[key] != default:
                print(f"Warning: invalid config value for '{key}'; using default.")
        for key in raw:
            if key.strip().lower() not in defaults:
                print(f"Warning: unknown config key '{key}' ignored.")
        return config
