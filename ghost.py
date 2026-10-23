"""Autonomous maze ghost with BFS chase and frightened behavior."""
from __future__ import annotations

import random
from collections import deque

import pygame


class Ghost:
    """A ghost that follows maze corridors and can flee while frightened."""

    def __init__(self, pos, pixel_pos, current_dir, target_pos, target_cell,
                 speed, collision, cell_size, color=(255, 65, 85)) -> None:
        self.position = tuple(pos)
        self.pixel_position = pygame.Vector2(pixel_pos)
        self.current_direction = current_dir
        self.target_position = target_pos
        self.target_cell = target_cell
        self.speed = float(speed)
        self.collision = collision
        self.cell_size = cell_size
        self.color = color
        self.frightened = False
        self.frightened_until = 0.0
        self.respawn_until = 0.0
        self.active = True
        self.home = tuple(pos)

    def get_next_direction(self, player_position):
        """Find a shortest legal step toward or away from the player."""
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        choices = []
        for direction in directions:
            if self.collision.can_move(self.position, direction):
                x, y = self.position
                neighbor = (x + direction[0], y + direction[1])
                distance = abs(neighbor[0] - player_position[0]) + abs(
                    neighbor[1] - player_position[1]
                )
                choices.append((distance, direction))
        if not choices:
            return None
        if self.frightened:
            farthest = max(item[0] for item in choices)
            return random.choice([d for dist, d in choices if dist == farthest])

        queue = deque([(self.position, None)])
        visited = {self.position}
        while queue:
            position, first_direction = queue.popleft()
            if position == tuple(player_position):
                return first_direction
            for direction in directions:
                if not self.collision.can_move(position, direction):
                    continue
                neighbor = (position[0] + direction[0], position[1] + direction[1])
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append((neighbor, direction if first_direction is None
                              else first_direction))
        return random.choice([d for _, d in choices])

    def reset(self, now: float = 0.0, delay: float = 0.0) -> None:
        """Return the ghost to its home corner."""
        self.position = self.home
        self.pixel_position = pygame.Vector2(
            (self.home[0] + 0.5) * self.cell_size,
            (self.home[1] + 0.5) * self.cell_size,
        )
        self.target_position = None
        self.target_cell = None
        self.active = delay <= 0
        self.respawn_until = now + delay

    def update(self, dt, player_position, now=0.0, frozen=False):
        """Advance the ghost one frame."""
        if not self.active:
            if now >= self.respawn_until:
                self.active = True
            else:
                return
        if frozen:
            return
        if self.frightened and now >= self.frightened_until:
            self.frightened = False
        if self.target_position is None:
            direction = self.get_next_direction(player_position)
            if direction is None:
                return
            self.current_direction = direction
            self.target_cell = (self.position[0] + direction[0],
                                self.position[1] + direction[1])
            self.target_position = pygame.Vector2(
                (self.target_cell[0] + 0.5) * self.cell_size,
                (self.target_cell[1] + 0.5) * self.cell_size,
            )
        offset = self.target_position - self.pixel_position
        distance = offset.length()
        step = self.speed * (0.55 if self.frightened else 1.0) * max(0.0, dt)
        if distance <= step:
            self.pixel_position = self.target_position.copy()
            self.position = self.target_cell
            self.target_position = None
            self.target_cell = None
        elif distance > 0 and step > 0:
            self.pixel_position += offset * (step / distance)

    def draw(self, screen, center):
        """Draw a simple rounded ghost sprite matching the game palette."""
        color = (65, 105, 255) if self.frightened else self.color
        radius = max(7, self.cell_size // 2 - 5)
        cx, cy = int(center[0]), int(center[1])
        pulse = 0.5 + 0.5 * __import__("math").sin(pygame.time.get_ticks() / 110.0)
        radius = max(6, radius + int(pulse * 1.2))
        pygame.draw.circle(screen, color, (cx, cy - 2), radius)
        pygame.draw.rect(screen, color, (cx - radius, cy - 2, radius * 2,
                                         radius + 4))
        foot_shift = int(pulse * 2)
        for index, offset in enumerate((-radius + 3, 0, radius - 3)):
            pygame.draw.circle(screen, color,
                               (cx + offset, cy + radius + (foot_shift if index % 2 else 0)), 4)
        eye_y = cy - 4
        for eye_x in (cx - radius // 3, cx + radius // 3):
            pygame.draw.circle(screen, (255, 255, 255), (eye_x, eye_y), 4)
            pygame.draw.circle(screen, (20, 35, 70), (eye_x, eye_y), 2)
