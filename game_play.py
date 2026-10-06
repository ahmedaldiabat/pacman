import pygame


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def draw_gameplay(self, background):
        self.screen.blit(background, (0, 0))
        pygame.draw.line(self.screen, (0, 80, 255), (250, 250), (250, 500), 10)
