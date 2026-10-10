import pygame
import menu
import instruction
import game_play


class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()
        self.selected = 0
        self.menu = menu.Menu(self.screen, self)
        self.background, self.button_list = self.menu.menu_init()
        self.state = "Menu"
        self.instruction = instruction.Instruction(self.screen)
        self.gameplay = game_play.Game(self.screen)
        self.pause_background = None

        self.pause_image = pygame.image.load(
            "materials/paused.png"
        ).convert_alpha()

        self.pause_image = pygame.transform.smoothscale(
            self.pause_image, (1100, 550)
        )

    def get_events(self):
        return pygame.event.get()

    def handle_menu_event(self, event):
        self.selected = self.menu.handle_event(event)

    def render_menu(self) -> None:
        self.menu.draw_menu()
        pygame.display.flip()

    def load_instruction(self):
        self.background = pygame.image.load(
            "materials/instruction_background.png"
        )
        self.background = pygame.transform.scale(self.background, (1600, 900))

    def render_instruction(self):
        if self.instruction.draw_instruction(self.background) == "back":
            self.state = "Menu"
        pygame.display.flip()

    def render_pause(self):
        if self.pause_background is None:
            return

        screen_size = self.screen.get_size()

        # Blur the captured gameplay screen.
        small_size = (
            max(1, screen_size[0] // 12),
            max(1, screen_size[1] // 12),
        )

        small = pygame.transform.smoothscale(
            self.pause_background, small_size
        )
        blurred = pygame.transform.smoothscale(
            small, screen_size
        )

        self.screen.blit(blurred, (0, 0))

        # Dark overlay.
        overlay = pygame.Surface(
            screen_size, pygame.SRCALPHA
        )
        overlay.fill((0, 0, 20, 110))
        self.screen.blit(overlay, (0, 0))

        # PAUSED graphic.
        image_rect = self.pause_image.get_rect(
            center=self.screen.get_rect().center
        )
        self.screen.blit(self.pause_image, image_rect)

        pygame.display.flip()

    def load_gameplay(self):
        self.background = pygame.image.load(
            "materials/GamePlay_background.png"
        )
        self.background = pygame.transform.scale(self.background, (1600, 900))

    def render_gameplay(self, maze: list[list[int]], player):
        self.gameplay.draw_gameplay(self.background, maze, player)
        pygame.display.flip()

    def quit(self) -> None:
        pygame.quit()
