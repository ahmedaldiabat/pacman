import pygame


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.cell_size = 43
        self.wall_width = 4
        self.wall_color = (65, 111, 168)
        self.player_color = (255, 220, 0)

    def cellWalls(self, walls: int) -> list[int]:
        """Return walls in North, East, South, West order."""
        return [
            1 if walls & 1 else 0,
            1 if walls & 2 else 0,
            1 if walls & 4 else 0,
            1 if walls & 8 else 0,
        ]

    def draw_gameplay(
        self,
        background: pygame.Surface,
        maze: list[list[int]],
        player=None,
    ) -> None:
        self.screen.blit(background, (0, 0))

        rows = len(maze)
        cols = len(maze[0]) if rows else 0
        if not cols:
            return

        self.maze_width = cols * self.cell_size
        self.maze_height = rows * self.cell_size
        start_x = (self.screen.get_width() - self.maze_width) // 2
        start_y = (self.screen.get_height() - self.maze_height) // 2

        for row in range(rows):
            y = start_y + row * self.cell_size
            for col in range(cols):
                x = start_x + col * self.cell_size
                walls = self.cellWalls(maze[row][col])

                # The maze generator uses 15 for cells in the 42 design.
                if maze[row][col] == 15:
                    pygame.draw.rect(
                        self.screen,
                        (245, 240, 230),
                        (x + 3, y + 3, self.cell_size - 6, self.cell_size - 6),
                        border_radius=4,
                    )
                    continue

                if walls[0]:  # North
                    pygame.draw.line(
                        self.screen, self.wall_color,
                        (x, y), (x + self.cell_size, y), self.wall_width,
                    )
                if walls[1]:  # East
                    pygame.draw.line(
                        self.screen, self.wall_color,
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        self.wall_width,
                    )
                if walls[2]:  # South
                    pygame.draw.line(
                        self.screen, self.wall_color,
                        (x, y + self.cell_size),
                        (x + self.cell_size, y + self.cell_size),
                        self.wall_width,
                    )
                if walls[3]:  # West
                    pygame.draw.line(
                        self.screen, self.wall_color,
                        (x, y), (x, y + self.cell_size), self.wall_width,
                    )

        if player is not None:
            px = round(start_x + player.pixel_position.x)
            py = round(start_y + player.pixel_position.y)
            pygame.draw.circle(
                self.screen,
                self.player_color,
                (px, py),
                max(6, self.cell_size // 3),
            )
