"""Instruction screen controls using the project's original back-button artwork."""
from __future__ import annotations

import pygame
from button import Button
import sounds


class Instruction:
    """Render the instruction background and a clickable back control."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        try:
            image = pygame.image.load("materials/back_button.png").convert_alpha()
            image = pygame.transform.smoothscale(image, (230, 78))
        except (pygame.error, OSError):
            image = pygame.Surface((230, 78), pygame.SRCALPHA)
            pygame.draw.rect(image, (35, 115, 160), image.get_rect(), border_radius=18)
            font = pygame.font.Font(None, 40)
            label = font.render("BACK", True, (255, 255, 255))
            image.blit(label, label.get_rect(center=image.get_rect().center))
        self.button = Button(image, 685, 790, screen)
        self.button.rect.topleft = (685, 790)
        self.button.draw_rect = self.button.image.get_rect(center=self.button.rect.center)
        self.button.glow_rect = self.button.draw_rect.inflate(-8, -8)

    def draw_instruction(self, background: pygame.Surface) -> bool:
        """Draw only the supplied artwork and back button; no extra text."""
        self.screen.blit(background, (0, 0))
        clicked = self.button.draw()
        if clicked:
            sounds.play(sounds.button_sound_on_click)
        return clicked

    def handle_event(self, event: pygame.event.Event):
        """Support keyboard back navigation."""
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_BACKSPACE
        ):
            sounds.play(sounds.button_sound_on_click)
            return "back"
        return None
