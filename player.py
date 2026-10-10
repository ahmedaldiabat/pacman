import pygame


class Player:
    def __init__(
        self,
        position,
        lives: int,
        cell_size: int = 43,
        speed: float = 150.0,
    ) -> None:
        self.position = (int(position[0]), int(position[1]))
        self.lives = lives
        self.cell_size = cell_size
        self.speed = speed
        # Pixel coordinates relative to the maze's top-left corner.
        self.pixel_position = pygame.Vector2(
            (self.position[0] + 0.5) * self.cell_size,
            (self.position[1] + 0.5) * self.cell_size,
        )
        self.target_position = None
        self.target_cell = None

    def update(self, direction, collision, dt: float) -> None:
        # Select a destination cell only when centered in the current cell.
        if self.target_position is None:
            if direction is None:
                return

            next_x = self.position[0] + direction[0]
            next_y = self.position[1] + direction[1]
            maze = collision.maze

            if not maze or not (0 <= next_y < len(maze)):
                return
            if not (0 <= next_x < len(maze[next_y])):
                return
            if not collision.can_move(self.position, direction):
                return

            self.target_cell = (next_x, next_y)
            self.target_position = pygame.Vector2(
                (next_x + 0.5) * self.cell_size,
                (next_y + 0.5) * self.cell_size,
            )

        # Move in pixels, independent of frame rate.
        offset = self.target_position - self.pixel_position
        distance = offset.length()
        step = self.speed * max(0.0, dt)

        if distance <= step:
            self.pixel_position = self.target_position.copy()
            self.position = self.target_cell
            self.target_position = None
            self.target_cell = None
        elif distance > 0 and step > 0:
            self.pixel_position += offset * (step / distance)
