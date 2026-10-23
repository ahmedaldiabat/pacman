*This activity has been created as part of the 42 curriculum by ahmedaldiabat.*

# Pac-Man — 42 Edition

## Description

A Python/Pygame recreation of the classic Pac-Man arcade game. The project keeps its original image-based main menu, blue maze walls, custom 42 maze motif, calm menu audio, and modular structure. The player collects pellets, avoids four ghosts, uses power pellets to frighten them, and progresses through ten levels.

## Features

- Image-based main menu with Start Game, High Scores, Instructions, and Exit.
- Keyboard navigation and mouse selection.
- Maze generated through the bundled `mazegenerator` package with `perfect=False`.
- Arrow keys or WASD movement, three starting lives, pellet scoring, and respawning.
- Four independently colored ghosts, chase/flee behavior, frightened-ghost scoring, and respawn delays.
- Ten levels, level timer, score/lives persistence between levels, pause/resume, and win/game-over screens.
- Persistent top-ten highscores with validated player names.
- Review cheat mode: press `C` during gameplay to toggle it; while enabled, `I` toggles invincibility, `F` freezes ghosts, `V` toggles speed boost, `L` skips a level, and `H` adds a life.
- Graceful fallbacks for missing audio/image assets and malformed configuration values.

## Instructions

Python 3.10+ is required. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Launch with exactly one configuration path:

```bash
python3 pac-man.py config.json
```

Alternatively, run `python3 main.py config.json`.

### Controls

- **Move:** Arrow keys or `W`, `A`, `S`, `D`
- **Pause / resume:** `P` or `Escape`; press `M` on the pause screen to return to the main menu
- **Menu navigation:** Up/down arrows, Enter/Space, or mouse
- **Cheat mode:** `C`, then `I`, `F`, `V`, `L`, or `H`
- **Save final score:** type a name (letters, digits, spaces; max 10 characters) and press Enter

## Configuration

The configuration is JSON with support for full-line `#` comments and `//` comments. Invalid values use defaults and unknown keys are ignored.

| Key | Default | Description |
|---|---:|---|
| `highscore_filename` | `highscores.json` | JSON file used to store the top ten |
| `levels` | Ten 15×15 levels | List of `{ "width": 15, "height": 15 }` objects; the game guarantees at least ten levels |
| `lives` | `3` | Starting lives |
| `pacgum` | `42` | Retained project configuration value |
| `points_per_pacgum` | `10` | Score for a small pellet |
| `points_per_super_pacgum` | `50` | Score for a power pellet |
| `points_per_ghost` | `200` | Score for eating a frightened ghost |
| `seed` | `42` | Deterministic first-level maze seed |
| `level_max_time` | `90` | Time limit per level in seconds |

Dimensions are capped to fit the existing 1600×900 window. The first level uses the configured seed; later levels use random seeds.

## Highscore

Scores are stored in a JSON array. On loading, malformed entries are ignored; entries are sorted by descending score and limited to ten. Player names are sanitized to letters, digits, and spaces, and truncated to ten characters. Saving uses a temporary file and atomic replacement to reduce the risk of a partially written score file.

## Maze Generation

The game imports `MazeGenerator` from `mazegenerator`. It requests `perfect=False` so the maze has loops suitable for arcade movement. The generator is used as supplied and is not altered by the game controller. The first level uses the configured seed, and later levels use randomly selected seeds. Generation errors are caught and fall back to a safe 15×15 maze.

## Implementation

- `main.py` / `pac-man.py`: command-line validation and startup.
- `parsing.py`: configuration comments, validation, and safe defaults.
- `game.py`: game state, level progression, input, scoring, collision response, and cheat controls.
- `player.py`: grid-aligned movement and Pac-Man sprite.
- `ghost.py`: ghost movement, chasing, frightened behavior, and drawing.
- `collision.py`: wall checks.
- `game_play.py`: maze, entities, pellets, and HUD rendering.
- `rendering.py`, `menu.py`, `button.py`, `instruction.py`: application screens and UI.
- `highscores.py`: persistent score table.
- `materials/`: original artwork and audio assets.
- `mazegenerator/`: supplied maze generator.

## General Software Architecture

`main` loads validated configuration, creates a `Renderer`, then constructs the `Game` controller. The controller owns the maze, player, ghosts, pellets, score, timer, and highscore storage. `Renderer` owns the Pygame display and delegates maze drawing to `game_play.Game`. The UI modules manage menu and instruction presentation. `Collision` is shared by player and ghosts to ensure movement respects maze walls.

## Project Management

The current project structure and feature checklist are maintained in the source repository. A manual acceptance checklist is provided in `docs/acceptance-tests.md`.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [Python documentation](https://docs.python.org/3/)
- [Python `json` documentation](https://docs.python.org/3/library/json.html)
- [Python `collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque)

AI assistance was used to audit the existing project against the activity specification, identify integration gaps, implement and document gameplay features, and prepare validation steps. The code should still be run and peer-reviewed in the target environment before submission.


## Recent integration fixes

- The gameplay renderer scales the maze to fit the 1600×900 viewport, and the simulation uses the same cell size as the renderer.
- The campaign length follows the configured `levels` array (the supplied configuration contains ten levels; configuration validation keeps at least ten levels).
- The instruction screen uses its artwork without extra overlaid instructional text. Its original back-button artwork works by mouse; Enter, Backspace, and Escape also return to the menu.
- The highscore screen uses the original menu background with a dark translucent panel, and its back button works by mouse. Enter, Backspace, and Escape return to the menu.
- Added synthesized, local WAV effects for normal pellets, power pellets, frightened ghosts being eaten, and the player being hit. Audio failures remain non-fatal.
- Added subtle Pac-Man chomping animation, pulsing power pellets, and animated ghost sprites.

## Controls

- Move: arrow keys or W/A/S/D.
- Pause/resume: P or Escape; press M from pause to return to the menu.
- Cheats: press C to enable cheat mode, then I (invincibility), F (freeze ghosts), V (speed boost), L (skip level), or H (extra life).
