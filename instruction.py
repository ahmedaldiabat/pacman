import pygame
import button


class Instruction:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("materials/back_button.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (301, 96))
        self.button = button.Button(self.image, 301, 96, self.screen)
