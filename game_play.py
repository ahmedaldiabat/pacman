import pygame


class Game:
    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        self.screen = screen
        self.cell_size = 43
        self.wall_width = 4
        self.wall_color = (65, 111, 168)

    def cellWalls(self, walls: int) -> list[int]:
        """Return walls in North, East, South, West order."""
        return [
            1 if walls & 1 else 0,  # North
            1 if walls & 2 else 0,  # East
            1 if walls & 4 else 0,  # South
            1 if walls & 8 else 0   # West
        ]

    def draw_gameplay(
        self,
        background: pygame.Surface,
        maze: list[list[int]]
    ) -> None:
        # Draw the background
        self.screen.blit(background, (0, 0))

        # Get maze dimensions
        rows = len(maze)
        cols = len(maze[0])

        # Calculate the total maze size in pixels
        self.maze_width = cols * self.cell_size
        self.maze_height = rows * self.cell_size

        # Center the maze on the screen
        start_x = (
            self.screen.get_width() - self.maze_width) // 2

        start_y = (
            self.screen.get_height() - self.maze_height) // 2

        # Draw each cell
        for row in range(rows):
            y = start_y + row * self.cell_size

            for col in range(cols):
                x = start_x + col * self.cell_size

                # Get the walls for this cell
                walls = self.cellWalls(maze[row][col])


                if maze[row][col] == 15:
                    pygame.draw.rect(
                        self.screen,
                        (245, 240, 230),
                        (
                            x + 3,
                            y + 3,
                            self.cell_size - 6,
                            self.cell_size - 6
                        ),
                        border_radius=4
                    )
                    continue

                if walls[0]:
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (x + self.cell_size, y),
                        self.wall_width
                    )

                # East
                if walls[1]:
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        self.wall_width
                    )

                # South
                if walls[2]:
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y + self.cell_size),
                        (x + self.cell_size, y + self.cell_size),
                        self.wall_width
                    )

                # West
                if walls[3]:
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (x, y + self.cell_size),
                        self.wall_width
                    )