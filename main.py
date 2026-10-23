"""Application entry point."""
from __future__ import annotations

import sys

import pygame
from parsing import Config
from rendering import Renderer
from game import Game


def main() -> int:
    """Launch the game with exactly one configuration-file argument."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return 2
    config = Config(sys.argv[1]).check_config()
    try:
        renderer = Renderer()
        game = Game(config, renderer)
        renderer.game_controller = game
        game.run()
    except (pygame.error, OSError, ValueError) as error:
        print(f"Pac-Man could not start: {error}")
        pygame.quit()
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
