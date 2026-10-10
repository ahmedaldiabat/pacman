import pygame
import button
import sounds


class Instruction:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("materials/Empty.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (340, 140))
        self.button = button.Button(self.image, 635, 770, self.screen)

    def draw_instruction(self, background):
        self.screen.blit(background, (0, 0))
        if self.button.draw():
            sounds.button_sound_on_click.play()
            return "back"
        self.button.glow()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "back"
