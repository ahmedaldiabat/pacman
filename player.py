import math

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
        self.current_direction = (1, 0)

    def update(self, direction, collision, dt: float) -> None:
        """
        Move toward the next cell center.

        A requested direction is treated as a turn request. If the turn is
        blocked, keep moving in the current direction instead.
        """
        if self.target_position is None:
            chosen_direction = None

            # Prefer the requested turn when it is legal.
            if direction is not None and self._can_move(
                collision, self.position, direction
            ):
                chosen_direction = direction

            # A blocked turn must not cancel movement.
            elif self._can_move(
                collision, self.position, self.current_direction
            ):
                chosen_direction = self.current_direction

            if chosen_direction is None:
                return

            next_x = self.position[0] + chosen_direction[0]
            next_y = self.position[1] + chosen_direction[1]
            self.target_cell = (next_x, next_y)
            self.target_position = pygame.Vector2(
                (next_x + 0.5) * self.cell_size,
                (next_y + 0.5) * self.cell_size,
            )
            self.current_direction = chosen_direction

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

    @staticmethod
    def _can_move(collision, position, direction) -> bool:
        x, y = position
        dx, dy = direction
        maze = collision.maze

        next_x = x + dx
        next_y = y + dy

        # Check bounds before querying the wall bits.
        if not maze or not (0 <= next_y < len(maze)):
            return False
        if not (0 <= next_x < len(maze[next_y])):
            return False

        return collision.can_move(position, direction)

    def draw(self, screen: pygame.Surface, center) -> None:
        """Draw Pac-Man facing the current movement direction."""
        import math

        radius = max(6, self.cell_size // 3)
        size = radius * 2 + 2
        cx = cy = size // 2

        # Black is transparent, so the maze remains visible through the mouth.
        sprite = pygame.Surface((size, size))
        sprite.fill((0, 0, 0))
        sprite.set_colorkey((0, 0, 0))

        yellow = (255, 220, 0)
        pygame.draw.circle(sprite, yellow, (cx, cy), radius)

        direction = self.current_direction or (1, 0)
        angle = math.atan2(direction[1], direction[0])
        mouth_angle = math.radians(28)

        mouth_points = [
            (cx, cy),
            (
                round(cx + radius * math.cos(angle - mouth_angle)),
                round(cy + radius * math.sin(angle - mouth_angle)),
            ),
            (
                round(cx + radius * math.cos(angle + mouth_angle)),
                round(cy + radius * math.sin(angle + mouth_angle)),
            ),
        ]

        # Remove the mouth wedge.
        pygame.draw.polygon(sprite, (0, 0, 0), mouth_points)

        screen.blit(
            sprite,
            (
                round(center[0] - size / 2),
                round(center[1] - size / 2),
            ),
        )

