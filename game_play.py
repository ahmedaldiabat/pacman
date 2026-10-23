"""Gameplay renderer; preserves the project's blue maze and themed background."""
from __future__ import annotations

import pygame


class Game:
    """Draw the maze, pellets, player, ghosts, and gameplay HUD."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.cell_size = 43
        self.wall_width = 4
        self.wall_color = (65, 111, 168)
        self.font = pygame.font.Font(None, 34)
        self.small_font = pygame.font.Font(None, 25)

    @staticmethod
    def cellWalls(walls: int) -> list[int]:
        """Return walls in North, East, South, West order."""
        return [int(bool(walls & bit)) for bit in (1, 2, 4, 8)]

    def maze_origin(self, maze):
        rows = len(maze)
        cols = len(maze[0]) if rows else 0
        size = min(43, (self.screen.get_width() - 100) // max(1, cols),
                   (self.screen.get_height() - 150) // max(1, rows))
        # Keep the maze inside the playable viewport even for custom dimensions.
        self.cell_size = max(8, size)
        size = self.cell_size
        return ((self.screen.get_width() - cols * size) // 2,
                95 + (self.screen.get_height() - 130 - rows * size) // 2,
                size)

    def draw_gameplay(self, background, maze, player=None, gums=None,
                      ghost=None, ghosts=None, score=0, lives=3, level=1,
                      remaining=90, cheat=False, total_levels=10):
        """Render a complete gameplay frame."""
        self.screen.blit(background, (0, 0))
        rows = len(maze)
        cols = len(maze[0]) if rows else 0
        if not cols:
            return
        start_x, start_y, cell = self.maze_origin(maze)
        self.cell_size = cell
        for row in range(rows):
            y = start_y + row * cell
            for col in range(cols):
                x = start_x + col * cell
                walls = self.cellWalls(maze[row][col])
                if maze[row][col] == 15:
                    pygame.draw.rect(self.screen, (245, 240, 230),
                                     (x + 3, y + 3, cell - 6, cell - 6),
                                     border_radius=4)
                    continue
                points = [
                    ((x, y), (x + cell, y)),
                    ((x + cell, y), (x + cell, y + cell)),
                    ((x, y + cell), (x + cell, y + cell)),
                    ((x, y), (x, y + cell)),
                ]
                for enabled, (a, b) in zip(walls, points):
                    if enabled:
                        pygame.draw.line(self.screen, self.wall_color, a, b,
                                         max(2, round(cell * 0.08)))
                if gums is not None and gums[row][col]:
                    center = (x + cell // 2, y + cell // 2)
                    if gums[row][col] == 1:
                        pygame.draw.circle(self.screen, (255, 220, 180),
                                           center, max(2, cell // 11))
                    elif gums[row][col] == 2:
                        # A soft pulse makes power pellets visibly animated.
                        pulse = 0.78 + 0.22 * (0.5 + 0.5 * __import__("math").sin(
                            pygame.time.get_ticks() / 130.0 + row + col))
                        radius = max(5, int(cell // 4 * pulse))
                        pygame.draw.circle(self.screen, (255, 170, 0),
                                           center, radius + max(2, cell // 12))
                        pygame.draw.circle(self.screen, (255, 235, 45),
                                           center, radius)
        if player is not None:
            player.draw(self.screen, (round(start_x + player.pixel_position.x),
                                      round(start_y + player.pixel_position.y)))
        all_ghosts = list(ghosts or ([] if ghost is None else [ghost]))
        for item in all_ghosts:
            if item.active:
                item.draw(self.screen, (round(start_x + item.pixel_position.x),
                                        round(start_y + item.pixel_position.y)))
        hud = (f"SCORE  {score:06d}     LIVES  {lives}     "
               f"LEVEL  {level}/{total_levels}     TIME  {max(0, int(remaining))}")
        text = self.font.render(hud, True, (255, 255, 255))
        self.screen.blit(text, (35, 24))
        if cheat:
            label = self.small_font.render("CHEAT MODE", True, (255, 210, 40))
            self.screen.blit(label, (self.screen.get_width() - 155, 58))

    def get_blurred_background(self):
        """Return a downscaled/upscaled copy for the pause overlay."""
        small = pygame.transform.smoothscale(
            self.screen, (max(1, self.screen.get_width() // 12),
                          max(1, self.screen.get_height() // 12)))
        return pygame.transform.smoothscale(small, self.screen.get_size())
