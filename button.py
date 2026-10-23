"""Reusable image button with a subtle yellow selection glow."""
from __future__ import annotations

import pygame
import sounds


class Button:
    """Image-backed button with hover, click, and focus feedback."""

    def __init__(self, image: pygame.Surface, x: int, y: int,
                 screen: pygame.Surface) -> None:
        self.screen = screen
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.clicked = False
        self.is_glowing = False
        self.played_sound = False

    def glow(self) -> None:
        """Draw a yellow border around the button."""
        pygame.draw.rect(self.screen, (255, 220, 0), self.rect.inflate(8, 8),
                         4, border_radius=20)
        self.screen.blit(self.image, self.rect)
        self.is_glowing = True

    def draw(self) -> bool:
        """Draw the button and return True on a fresh left click."""
        position = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(position)
        if hover:
            self.glow()
            if not self.played_sound:
                sounds.play(sounds.button_sound_on_select)
                self.played_sound = True
        else:
            self.screen.blit(self.image, self.rect)
            self.played_sound = False
            self.is_glowing = False
        pressed = pygame.mouse.get_pressed()[0]
        action = hover and pressed and not self.clicked
        if action:
            self.clicked = True
        if not pressed:
            self.clicked = False
        return bool(action)
