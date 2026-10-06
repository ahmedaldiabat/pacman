import pygame
from button import Button
import game
import sounds

class Menu:
    def __init__(self, screen: pygame.Surface, renderer) -> None:
        self.screen = screen
        self.selected = 0
        self.background = None
        self.buttons: list[Button] = []
        self.game = game
        self.renderer = renderer
        pygame.mixer.init()

    def buttons_init(self) -> dict[str, Button]:
        buttons_dict = {}

        start_button = pygame.image.load(
            "materials/start_button.png").convert()
        start_button.set_colorkey((0, 0, 0))
        start_button = pygame.transform.scale(start_button, (500, 200))

        high_scores_button = pygame.image.load(
            "materials/HighScores_button.png").convert()
        high_scores_button.set_colorkey((0, 0, 0))
        high_scores_button = pygame.transform.scale(
            high_scores_button, (500, 200))

        instruction_button = pygame.image.load(
            "materials/instructions_button.png")
        instruction_button.set_colorkey((0, 0, 0))
        instruction_button = pygame.transform.scale(
            instruction_button, (500, 200))

        exit_button = pygame.image.load(
            "materials/exit_button.png").convert()
        exit_button.set_colorkey((0, 0, 0))
        exit_button = pygame.transform.scale(exit_button, (500, 200))

        buttons_dict["start"] = Button(start_button, 30, 50, self.screen)
        buttons_dict["exit"] = Button(exit_button, 30, 650, self.screen)
        buttons_dict["HighScore"] = Button(
            high_scores_button, 30, 250, self.screen)
        buttons_dict["instruction"] = Button(
            instruction_button, 30, 450, self.screen)

        return buttons_dict

    def menu_init(self):
        pygame.mixer.music.load("materials/pacman_menu_calm.wav")
        pygame.mixer.music.play(-1)

        self.background = pygame.image.load("materials/BackGround.png")
        self.background = pygame.transform.scale(self.background, (1600, 900))

        buttons_dict = self.buttons_init()
        self.buttons = [
            buttons_dict["start"],
            buttons_dict["HighScore"],
            buttons_dict["instruction"],
            buttons_dict["exit"]
        ]
        return self.background, self.buttons

    def draw_menu(self) -> None:
        self.screen.blit(self.background, (0, 0))

        if self.buttons[0].draw():
            sounds.button_sound_on_click.play()
            self.renderer.state = "gameplay"
            self.renderer.load_gameplay()

        if self.buttons[1].draw():
            sounds.button_sound_on_click.play()

        if self.buttons[2].draw():
            sounds.button_sound_on_click.play()
            self.renderer.state = "Instruction"
            self.renderer.load_instruction()

        if self.buttons[3].draw():
            sounds.button_sound_on_click.play()
            pygame.quit()
            raise SystemExit

        self.buttons[self.selected].glow()
        self.buttons[self.selected].is_glowing = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 4
                sounds.button_sound_on_select.play()
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % 4
                sounds.button_sound_on_select.play()
            elif event.key == pygame.K_RETURN:
                sounds.button_sound_on_click.play()
                if self.selected == 2:
                    sounds.button_sound_on_click.play()
                    self.renderer.state = "Instruction"
                    self.renderer.load_instruction()
                if self.selected == 3:
                    pygame.quit()
                    raise SystemExit
                if self.selected == 0:
                    sounds.button_sound_on_click.play()
                    self.renderer.state = "gameplay"
                    self.renderer.load_gameplay()
