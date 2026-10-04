import pygame


class Button:
    def __init__(self, image: pygame.Surface, x: int, y: int,
                 screen: pygame.Surface) -> None:
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))
        self.clicked = False
        self.screen = screen
        self.is_glowing = False
        self.played_sound = False

    def glow(self) -> None:
        width = int(self.image.get_width() * 1.05)
        height = int(self.image.get_height() * 1.05)

        image = pygame.transform.smoothscale(self.image, (width, height))
        draw_rect = image.get_rect(center=self.rect.center)
        glow_rect = draw_rect.inflate(-16, -16)

        pygame.draw.rect(self.screen, (255, 220, 0), glow_rect,
                         4, border_radius=20)
        self.screen.blit(image, draw_rect)
        self.is_glowing = True

    def draw(self, select_sound: pygame.mixer.Sound) -> bool:
        action = False
        pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(pos)

        if hover:
            self.glow()
            if not self.played_sound:
                select_sound.play()
                self.played_sound = True
            self.is_glowing = False
        elif not self.is_glowing:
            self.screen.blit(self.image, self.rect)
            self.played_sound = False

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
