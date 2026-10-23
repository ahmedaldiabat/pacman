"""Persistent, validated top-ten highscore storage."""
from __future__ import annotations

import json
import os
import re
from typing import Any


class Highscores:
    """Load, validate, rank, and save highscore entries."""

    def __init__(self, filename: str = "highscores.json") -> None:
        self.filename = filename
        self.entries: list[dict[str, Any]] = []
        self.load()

    @staticmethod
    def valid_name(name: str) -> str:
        """Normalize a name to at most ten alphanumeric characters/spaces."""
        name = re.sub(r"[^A-Za-z0-9 ]", "", name)[:10].strip()
        return name or "PLAYER"

    def load(self) -> list[dict[str, Any]]:
        """Load valid entries; recover safely from missing or malformed files."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                raw = json.load(file)
            if not isinstance(raw, list):
                raise ValueError("highscore data must be a list")
            entries = []
            for item in raw:
                if not isinstance(item, dict):
                    continue
                name, score = item.get("name"), item.get("score")
                if (isinstance(name, str) and isinstance(score, int)
                        and not isinstance(score, bool) and score >= 0):
                    entries.append({
                        "name": self.valid_name(name),
                        "score": score,
                    })
            self.entries = sorted(
                entries, key=lambda item: item["score"], reverse=True
            )[:10]
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self.entries = []
        return self.entries

    def add(self, name: str, score: int) -> None:
        """Add a valid score and persist the top ten entries."""
        if not isinstance(score, int) or isinstance(score, bool) or score < 0:
            return
        self.entries.append({"name": self.valid_name(name), "score": score})
        self.entries.sort(key=lambda item: item["score"], reverse=True)
        self.entries = self.entries[:10]
        directory = os.path.dirname(os.path.abspath(self.filename))
        try:
            os.makedirs(directory, exist_ok=True)
            temp_name = self.filename + ".tmp"
            with open(temp_name, "w", encoding="utf-8") as file:
                json.dump(self.entries, file, indent=2)
            os.replace(temp_name, self.filename)
        except OSError as error:
            print(f"Warning: could not save highscores: {error}")
