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

    def get_events(self):
        return pygame.event.get()

    def handle_menu_event(self, event):
        self.selected = self.menu.handle_event(event)

    def render_menu(self) -> None:
        self.menu.draw_menu()
        pygame.display.flip()
        self.clock.tick(60)

    def load_instruction(self):
        self.background = pygame.image.load("materials/instruction_background.png")
        self.background = pygame.transform.scale(self.background, (1600, 900))

    def render_instruction(self):
        if self.instruction.draw_instruction(self.background) == "back":
            self.state = "Menu"
        pygame.display.flip()
        self.clock.tick(60)

    def load_gameplay(self):
        self.background = pygame.image.load("materials/GamePlay_background.png")
        self.background = pygame.transform.scale(self.background, (1600, 900))

    def render_gameplay(self, maze: list[list[int]]):
        self.gameplay.draw_gameplay(self.background, maze)
        pygame.display.flip()
        self.clock.tick(60)


    def quit(self) -> None:
        pygame.quit()
