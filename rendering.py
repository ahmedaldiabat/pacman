import pygame
import menu

class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()
        self.selected = 0
        self.background, self.button_list = menu.Menu.menu_init(self.screen)
    
    def get_events(self):
        return pygame.event.get()

    def handle_menu_event(self, event):
        self.selected = menu.Menu.handle_event(
            event,
            self.selected
            )

    def render_menu(self) -> None:
        menu.Menu.draw_menu(
            self.screen,
            self.selected,
            self.background,
            self.button_list
        )
        pygame.display.flip()
        self.clock.tick(60)

    def quit(self) -> None:
        pygame.quit()
