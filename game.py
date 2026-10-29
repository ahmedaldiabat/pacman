"""Game controller for the existing Pac-Man project."""
from __future__ import annotations

import random
import pygame

from collision import Collision
from ghost import Ghost
from highscores import Highscores
from mazegenerator import MazeGenerator
from player import Player
import sounds


class Game:
    """Own gameplay state, progression, input, and screen transitions."""

    GHOST_COLORS = [(255, 65, 85), (255, 150, 205),
                    (70, 220, 235), (255, 165, 55)]

    def __init__(self, config, renderer) -> None:
        self.config = config
        self.renderer = renderer
        self.running = True
        self.state_before_pause = "gameplay"
        self.highscores = Highscores(config["highscore_filename"])
        self.score = 0
        self.level_index = 0
        self.lives = config["lives"]
        self.level_elapsed = 0.0
        self.direction = None
        self.respawn_protection = 0.0
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False
        self.speed_boost = False
        self.name_entry = ""
        self.end_message = ""
        self.levels = config["levels"]
        self.renderer.load_gameplay()
        self._create_level(0)

    def player_start_pos(self):
        """Find a walkable cell nearest the maze center."""
        height, width = len(self.maze), len(self.maze[0])
        candidates = sorted(
            ((x, y) for y in range(height) for x in range(width)
             if self.maze[y][x] != 15),
            key=lambda p: abs(p[0] - width // 2) + abs(p[1] - height // 2),
        )
        for x, y in candidates:
            if any(self.collision.can_move((x, y), d)
                   for d in ((0, -1), (1, 0), (0, 1), (-1, 0))):
                return x, y
        return candidates[0] if candidates else (1, 1)

    def _create_level(self, index: int) -> None:
        """Generate a level using the bundled A-Maze-ing package."""
        self.level_index = index
        level = self.levels[min(index, len(self.levels) - 1)]
        width, height = level["width"], level["height"]
        seed = self.config["seed"] if index == 0 else random.randint(1, 2**31 - 1)
        try:
            self.maze_generator = MazeGenerator(
                size=(width, height), perfect=False, seed=seed
            )
            self.maze = self.maze_generator.maze
        except Exception as error:
            print(f"Warning: maze generation failed ({error}); using safe fallback.")
            self.maze_generator = MazeGenerator(size=(15, 15), perfect=False,
                                                 seed=42)
            self.maze = self.maze_generator.maze
        self.collision = Collision(self.maze)
        # Fit first, so simulation coordinates and rendered cell size agree.
        self.renderer.gameplay.maze_origin(self.maze)
        self.player = Player(self.player_start_pos(), self.lives,
                             cell_size=self.renderer.gameplay.cell_size)
        self.player.speed = 150.0 + min(index, 5) * 5
        self.gums = self._init_gums()
        self.ghosts = []
        walkable = [(x, y) for y, row in enumerate(self.maze)
                    for x, value in enumerate(row)
                    if value != 15 and (x, y) != self.player.position]
        corners = [(1, 1), (len(self.maze[0]) - 2, 1),
                   (1, len(self.maze) - 2),
                   (len(self.maze[0]) - 2, len(self.maze) - 2)]
        used = {self.player.position}
        for number, corner in enumerate(corners):
            pos = corner if corner in walkable else min(
                walkable or [self.player.position],
                key=lambda p: abs(p[0] - corner[0]) + abs(p[1] - corner[1]))
            if pos in used:
                pos = next((p for p in walkable if p not in used), pos)
            used.add(pos)
            self.ghosts.append(Ghost(
                pos=pos,
                pixel_pos=pygame.Vector2((pos[0] + 0.5) *
                                         self.renderer.gameplay.cell_size,
                                         (pos[1] + 0.5) *
                                         self.renderer.gameplay.cell_size),
                current_dir=(0, 1), target_pos=None, target_cell=None,
                speed=85.0 + number * 3 + index * 2, collision=self.collision,
                cell_size=self.renderer.gameplay.cell_size,
                color=self.GHOST_COLORS[number],
            ))
        self.ghost = self.ghosts[0]
        self.level_elapsed = 0.0
        self.direction = None
        self.respawn_protection = 1.5

    def _init_gums(self):
        """Place pellets in walkable cells and power pellets near the corners."""
        height, width = len(self.maze), len(self.maze[0])
        gums = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                if self.maze[y][x] != 15 and (x, y) != self.player.position:
                    gums[y][x] = 1
        corners = [(1, 1), (width - 2, 1), (1, height - 2),
                   (width - 2, height - 2)]
        for x, y in corners:
            if 0 <= y < height and 0 <= x < width and self.maze[y][x] != 15:
                gums[y][x] = 2
        return gums

    def start_game(self) -> None:
        """Start a fresh run and reset score, lives, and level."""
        self.score = 0
        self.lives = self.config["lives"]
        self.cheat_mode = self.invincible = self.ghosts_frozen = False
        self.speed_boost = False
        self.name_entry = ""
        self._create_level(0)
        self.renderer.state = "gameplay"

    def _finish(self, won: bool) -> None:
        self.end_message = "YOU WIN!" if won else "GAME OVER"
        self.renderer.state = "gameover"
        self.name_entry = ""

    def _next_level(self) -> None:
        # The config controls the campaign length; the default config has 10 levels.
        if self.level_index + 1 >= len(self.levels):
            self._finish(True)
            return
        self._create_level(self.level_index + 1)
        self.renderer.state = "gameplay"

    def _respawn(self) -> None:
        self.lives -= 1
        self.player.lives = self.lives
        if self.lives <= 0:
            self._finish(False)
            return
        self.player.position = self.player_start_pos()
        self.player.pixel_position = pygame.Vector2(
            (self.player.position[0] + 0.5) * self.player.cell_size,
            (self.player.position[1] + 0.5) * self.player.cell_size)
        self.player.target_position = self.player.target_cell = None
        self.player.current_direction = (0, 1)
        for ghost in self.ghosts:
            ghost.reset(self.level_elapsed, random.uniform(0.2, 1.0))
        self.respawn_protection = 2.0

    def _check_ghost_collisions(self) -> None:
        if self.respawn_protection > 0:
            return
        for ghost in self.ghosts:
            if not ghost.active:
                continue
            distance = self.player.pixel_position.distance_to(ghost.pixel_position)
            if distance < self.player.cell_size * 0.58:
                if ghost.frightened:
                    self.score += self.config["points_per_ghost"]
                    sounds.play(sounds.ghost_eaten_sound)
                    ghost.reset(self.level_elapsed, 5.0)
                elif not self.invincible:
                    sounds.play(sounds.player_hit_sound)
                    self._respawn()
                return

    def update(self, dt: float) -> None:
        """Update only while the game is actively being played."""
        if self.renderer.state != "gameplay":
            return
        self.level_elapsed += dt
        self.respawn_protection = max(0.0, self.respawn_protection - dt)
        self.player.speed = 225.0 if self.speed_boost else 150.0 + min(
            self.level_index, 5) * 5
        arrived = self.player.update(self.direction, self.collision, dt)
        if arrived is not None:
            x, y = arrived
            gum = self.gums[y][x]
            if gum == 1:
                self.score += self.config["points_per_pacgum"]
                self.gums[y][x] = 0
                sounds.play(sounds.pacgum_sound)
            elif gum == 2:
                self.score += self.config["points_per_super_pacgum"]
                self.gums[y][x] = 0
                sounds.play(sounds.power_pellet_sound)
                for ghost in self.ghosts:
                    ghost.frightened = True
                    ghost.frightened_until = self.level_elapsed + 7.0
            if not any(gum for row in self.gums for gum in row):
                self._next_level()
                return
        for ghost in self.ghosts:
            ghost.update(dt, self.player.position, self.level_elapsed,
                         self.ghosts_frozen)
        self._check_ghost_collisions()
        if self.level_elapsed >= self.config["level_max_time"]:
            self._finish(False)

    def handle_events(self, events) -> None:
        """Dispatch keyboard and mouse events for every game screen."""
        directions = {
            pygame.K_w: (0, -1), pygame.K_UP: (0, -1),
            pygame.K_s: (0, 1), pygame.K_DOWN: (0, 1),
            pygame.K_a: (-1, 0), pygame.K_LEFT: (-1, 0),
            pygame.K_d: (1, 0), pygame.K_RIGHT: (1, 0),
        }
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                continue
            if event.type == pygame.KEYDOWN:
                state = self.renderer.state
                if state == "Menu":
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else:
                        self.renderer.menu.handle_event(event)
                elif state == "Instruction":
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE,
                                     pygame.K_RETURN):
                        self.renderer.state = "Menu"
                elif state == "Highscores":
                    if event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE,
                                     pygame.K_RETURN):
                        self.renderer.state = "Menu"
                elif state == "gameplay":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.renderer.capture_pause_background()
                        self.renderer.state = "pause"
                    elif event.key in directions:
                        self.direction = directions[event.key]
                    elif event.key == pygame.K_c:
                        self.cheat_mode = not self.cheat_mode
                        if not self.cheat_mode:
                            self.invincible = self.ghosts_frozen = self.speed_boost = False
                    elif self.cheat_mode:
                        # Number keys are the simple, documented cheat controls.
                        # Keep the letter shortcuts for existing users.
                        if event.key in (pygame.K_1, pygame.K_i):
                            self.invincible = not self.invincible
                        elif event.key == pygame.K_f:
                            self.ghosts_frozen = not self.ghosts_frozen
                        elif event.key == pygame.K_v:
                            self.speed_boost = not self.speed_boost
                        elif event.key in (pygame.K_2, pygame.K_l):
                            self._next_level()
                        elif event.key == pygame.K_h:
                            self.lives += 1
                            self.player.lives = self.lives
                elif state == "pause":
                    if event.key in (pygame.K_ESCAPE, pygame.K_p, pygame.K_RETURN):
                        self.renderer.state = "gameplay"
                    elif event.key == pygame.K_m:
                        self.renderer.state = "Menu"
                elif state == "gameover":
                    if event.key == pygame.K_RETURN:
                        self.highscores.add(self.name_entry, self.score)
                        self.renderer.state = "Menu"
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_entry = self.name_entry[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        char = event.unicode
                        if (char.isalnum() or char == " ") and len(self.name_entry) < 10:
                            self.name_entry += char
            elif self.renderer.state == "Menu":
                self.renderer.menu.handle_event(event)
            elif self.renderer.state == "Instruction":
                if self.renderer.instruction.handle_event(event) == "back":
                    self.renderer.state = "Menu"

    def run(self) -> None:
        """Run the shared fixed-rate event/update/render loop."""
        try:
            while self.running:
                dt = min(self.renderer.clock.tick(60) / 1000.0, 0.05)
                events = self.renderer.get_events()
                self.handle_events(events)
                self.update(dt)
                state = self.renderer.state
                if state == "Menu":
                    self.renderer.render_menu()
                elif state == "Instruction":
                    self.renderer.render_instruction()
                elif state == "Highscores":
                    self.renderer.render_highscores(self.highscores.entries)
                elif state == "gameplay":
                    self.renderer.render_gameplay(
                        self.maze, self.player, self.gums, self.ghost,
                        ghosts=self.ghosts, score=self.score, lives=self.lives,
                        level=self.level_index + 1,
                        total_levels=len(self.levels),
                        remaining=self.config["level_max_time"] - self.level_elapsed,
                        cheat=self.cheat_mode,
                    )
                elif state == "pause":
                    self.renderer.render_pause()
                elif state == "gameover":
                    self.renderer.render_gameover(
                        self.end_message, self.score, self.name_entry)
        finally:
            self.renderer.quit()
