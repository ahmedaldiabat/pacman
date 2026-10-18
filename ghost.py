
import pygame
from collections import deque


class Ghost:
    def __init__(
        self,
        pos,
        pixel_pos,
        current_dir,
        target_pos,
        target_cell,
        speed,
        collision,
        cell_size,
    ):
        self.position = pos
        self.pixel_position = pixel_pos
        self.current_direction = current_dir
        self.target_position = target_pos
        self.target_cell = target_cell
        self.speed = speed
        self.collision = collision
        self.cell_size = cell_size

    def get_next_direction(self, player_position):
        directions = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0),
        ]

        queue = deque([(self.position, None)])
        visited = {self.position}

        while queue:
            position, first_direction = queue.popleft()

            if position == player_position:
                return first_direction

            for direction in directions:
                if not self.collision.can_move(position, direction):
                    continue

                x, y = position
                dx, dy = direction
                neighbor = (x + dx, y + dy)

                if neighbor in visited:
                    continue

                visited.add(neighbor)
                next_direction = (
                    direction
                    if first_direction is None
                    else first_direction
                )

                queue.append((neighbor, next_direction))

        return None

    def update(self, dt, player_position):
        if self.target_position is None:
            direction = self.get_next_direction(player_position)

            if direction is None:
                return

            self.current_direction = direction

            x, y = self.position
            dx, dy = direction

            self.target_cell = (x + dx, y + dy)
            self.target_position = pygame.Vector2(
                (self.target_cell[0] + 0.5) * self.cell_size,
                (self.target_cell[1] + 0.5) * self.cell_size,
            )

        offset = self.target_position - self.pixel_position
        distance = offset.length()
        step = self.speed * dt

        if distance <= step:
            self.pixel_position = self.target_position.copy()
            self.position = self.target_cell
            self.target_position = None
            self.target_cell = None
        elif distance > 0:
            self.pixel_position += offset * (step / distance)
