"""Pygame renderer for menus, gameplay, pause, highscores, and game endings."""
from __future__ import annotations

import pygame
import game_play
import instruction
import menu


class Renderer:
    """Own the display and render individual application states."""

    def __init__(self) -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen: pygame.Surface = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("PacMan - 42 Edition")
        self.clock = pygame.time.Clock()
        self.selected = 0
        self.state = "Menu"
        self.game_controller = None
        self.menu = menu.Menu(self.screen, self)
        self.background, self.button_list = self.menu.menu_init()
        self.instruction = instruction.Instruction(self.screen)
        self.gameplay = game_play.Game(self.screen)
        self.pause_background = None
        self.background = self._load_image("materials/BackGround.png")
        self._menu_background = self.background
        self.gameplay_background = self._load_image(
            "materials/GamePlay_background.png")
        self.instruction_background = self._load_image(
            "materials/instruction_background.png")
        self.pause_image = self._load_image("materials/paused.png", alpha=True)
        self.pause_image = pygame.transform.smoothscale(self.pause_image, (850, 425))
        self.font = pygame.font.Font(None, 58)
        self.medium_font = pygame.font.Font(None, 38)
        self.small_font = pygame.font.Font(None, 30)
        self.highscore_back_button = self._make_back_button((685, 790))

    def _load_image(self, path: str, alpha: bool = False) -> pygame.Surface:
        """Load a local asset and scale it to the display; report missing files."""
        try:
            image = pygame.image.load(path)
            image = image.convert_alpha() if alpha else image.convert()
            return pygame.transform.smoothscale(image, self.screen.get_size())
        except (pygame.error, OSError) as error:
            print(f"Warning: cannot load {path}: {error}")
            image = pygame.Surface(self.screen.get_size())
            image.fill((8, 10, 28))
            return image

    def get_events(self):
        return pygame.event.get()

    def handle_menu_event(self, event):
        self.selected = self.menu.handle_event(event)

    def render_menu(self) -> None:
        self.menu.draw_menu()
        pygame.display.flip()

    def _make_back_button(self, position):
        from button import Button
        try:
            image = pygame.image.load("materials/back_button.png").convert_alpha()
            image = pygame.transform.smoothscale(image, (230, 78))
        except (pygame.error, OSError):
            image = pygame.Surface((230, 78), pygame.SRCALPHA)
            pygame.draw.rect(image, (35, 115, 160), image.get_rect(), border_radius=18)
            label = self.medium_font.render("BACK", True, (255, 255, 255))
            image.blit(label, label.get_rect(center=image.get_rect().center))
        item = Button(image, *position, self.screen)
        item.rect.topleft = position
        item.draw_rect = item.image.get_rect(center=item.rect.center)
        item.glow_rect = item.draw_rect.inflate(-8, -8)
        return item

    def load_instruction(self) -> None:
        # Do not overwrite the menu background: returning to the menu/highscores
        # must restore the correct artwork.
        self.state = "Instruction"

    def render_instruction(self) -> None:
        if self.instruction.draw_instruction(self.instruction_background):
            self.state = "Menu"
        pygame.display.flip()

    def load_gameplay(self) -> None:
        self.background = self.gameplay_background

    def render_gameplay(self, maze, player, gums, ghost=None, **kwargs) -> None:
        self.gameplay.draw_gameplay(self.gameplay_background, maze, player,
                                    gums, ghost, **kwargs)
        pygame.display.flip()

    def capture_pause_background(self) -> None:
        self.pause_background = self.screen.copy()

    def render_pause(self) -> None:
        if self.pause_background is not None:
            small_size = (max(1, self.screen.get_width() // 12),
                          max(1, self.screen.get_height() // 12))
            blurred = pygame.transform.smoothscale(
                pygame.transform.smoothscale(self.pause_background, small_size),
                self.screen.get_size())
            self.screen.blit(blurred, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 145))
        self.screen.blit(overlay, (0, 0))
        image_rect = self.pause_image.get_rect(center=(800, 350))
        self.screen.blit(self.pause_image, image_rect)
        lines = ["ENTER / P / ESC  -  RESUME", "M  -  MAIN MENU"]
        for i, line in enumerate(lines):
            text = self.medium_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(800, 670 + i * 48)))
        pygame.display.flip()

    def render_highscores(self, entries) -> None:
        # Use the original menu artwork with a dark translucent panel for contrast.
        self.screen.blit(self._load_cached_background(), (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (4, 8, 28, 205), (430, 70, 740, 760),
                         border_radius=28)
        pygame.draw.rect(overlay, (65, 190, 220, 220), (430, 70, 740, 760),
                         width=3, border_radius=28)
        self.screen.blit(overlay, (0, 0))
        title = self.font.render("HIGH SCORES", True, (255, 220, 0))
        self.screen.blit(title, title.get_rect(center=(800, 135)))
        entries = entries or []
        for index in range(10):
            if index < len(entries):
                item = entries[index]
                line = f"{index + 1:>2}.  {item['name']:<10}  {item['score']:>8}"
            else:
                line = f"{index + 1:>2}.  ---"
            text = self.medium_font.render(line, True, (245, 245, 255))
            self.screen.blit(text, text.get_rect(center=(800, 220 + index * 48)))
        if self.highscore_back_button.draw():
            import sounds
            sounds.play(sounds.button_sound_on_click)
            self.state = "Menu"
        pygame.display.flip()

    def _load_cached_background(self):
        """Return the original menu background, never the instruction artwork."""
        return self._menu_background


    def render_gameover(self, message: str, score: int, name: str) -> None:
        self.screen.blit(self.gameplay_background, (0, 0))
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 18, 205))
        self.screen.blit(overlay, (0, 0))
        color = (255, 220, 0) if "WIN" in message else (255, 75, 90)
        title = self.font.render(message, True, color)
        self.screen.blit(title, title.get_rect(center=(800, 270)))
        score_text = self.medium_font.render(f"FINAL SCORE: {score}", True,
                                             (255, 255, 255))
        self.screen.blit(score_text, score_text.get_rect(center=(800, 365)))
        prompt = self.medium_font.render("ENTER NAME (10 characters max):",
                                         True, (255, 255, 255))
        self.screen.blit(prompt, prompt.get_rect(center=(800, 465)))
        entry = self.font.render((name or "_"), True, (255, 220, 0))
        self.screen.blit(entry, entry.get_rect(center=(800, 530)))
        footer = self.small_font.render("ENTER - SAVE SCORE AND RETURN TO MENU",
                                        True, (220, 230, 255))
        self.screen.blit(footer, footer.get_rect(center=(800, 640)))
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
