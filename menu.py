"""Main menu preserving the project's image-based button style."""
from __future__ import annotations

import pygame
from button import Button
import sounds


class Menu:
    """Display and route the four main menu actions."""

    def __init__(self, screen: pygame.Surface, renderer) -> None:
        self.screen = screen
        self.selected = 0
        self.background = None
        self.buttons: list[Button] = []
        self.renderer = renderer

    def buttons_init(self) -> dict[str, Button]:
        """Load the original button artwork and place it consistently."""
        specs = [
            ("start", "materials/start_button.png", 30, 50),
            ("HighScore", "materials/HighScores_button.png", 30, 250),
            ("instruction", "materials/instructions_button.png", 30, 450),
            ("exit", "materials/exit_button.png", 30, 650),
        ]
        result = {}
        for name, path, x, y in specs:
            try:
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.smoothscale(image, (500, 150))
            except (pygame.error, OSError) as error:
                print(f"Warning: cannot load menu button {path}: {error}")
                image = pygame.Surface((500, 150), pygame.SRCALPHA)
                font = pygame.font.Font(None, 48)
                label = font.render(name.upper(), True, (255, 220, 0))
                image.blit(label, label.get_rect(center=(250, 75)))
            result[name] = Button(image, x, y, self.screen)
        return result

    def menu_init(self):
        """Initialize background music and original menu assets."""
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.load("materials/pacman_menu_calm.wav")
                pygame.mixer.music.set_volume(0.25)
                pygame.mixer.music.play(-1)
        except (pygame.error, OSError):
            pass
        try:
            self.background = pygame.image.load(
                "materials/BackGround.png").convert()
            self.background = pygame.transform.smoothscale(
                self.background, self.screen.get_size())
        except (pygame.error, OSError):
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((8, 10, 28))
        buttons = self.buttons_init()
        self.buttons = [buttons["start"], buttons["HighScore"],
                        buttons["instruction"], buttons["exit"]]
        return self.background, self.buttons

    def _activate(self, index: int) -> None:
        """Run the action associated with a menu index."""
        sounds.play(sounds.button_sound_on_click)
        if index == 0:
            self.renderer.game_controller.start_game()
        elif index == 1:
            self.renderer.state = "Highscores"
        elif index == 2:
            self.renderer.state = "Instruction"
            self.renderer.load_instruction()
        elif index == 3:
            self.renderer.game_controller.running = False

    def draw_menu(self) -> None:
        self.screen.blit(self.background, (0, 0))
        mouse_position = pygame.mouse.get_pos()
        for index, button in enumerate(self.buttons):
            if button.draw():
                self.selected = index
                self._activate(index)
            if button.rect.collidepoint(mouse_position):
                self.selected = index
        if self.buttons:
            self.buttons[self.selected].glow()
            self.buttons[self.selected].is_glowing = False

    def handle_event(self, event: pygame.event.Event) -> int:
        """Support keyboard navigation and mouse clicks."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
                sounds.play(sounds.button_sound_on_select)
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
                sounds.play(sounds.button_sound_on_select)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate(self.selected)
        return self.selected
