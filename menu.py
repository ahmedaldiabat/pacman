import pygame 
 
class Menu(): 
    def __init__(self, image: pygame.Surface, x: int, y: int, screen: pygame.Surface) -> None: 
        self.image = image 
        self.rect = image.get_rect(topleft=(x, y)) 
        self.clicked = False 
        self.screen = screen 
        self.is_glowing = False
    pygame.mixer.init()
    button_sound_on_select = pygame.mixer.Sound(
        "materials/pacman_button_select.wav"
    )
    button_sound_on_select.set_volume(0.7)
    button_sound_on_click = pygame.mixer.Sound(
        "materials/pacman_button_click.wav"
    )

    def glow(self) -> None: 
        width = int(self.image.get_width() * 1.05) 
        height = int(self.image.get_height() * 1.05) 
 
        image = pygame.transform.smoothscale( 
            self.image, (width, height)) 
 
        draw_rect = image.get_rect(center=self.rect.center) 
 
        glow_rect = draw_rect.inflate(-16, -16) 
 
        pygame.draw.rect( 
            self.screen, 
            (255, 220, 0), 
            glow_rect, 
            4, 
            border_radius=20) 
        self.screen.blit(image, draw_rect) 
        self.is_glowing = True 
 
    def draw(self) -> bool: 
        action = False 
 
        pos = pygame.mouse.get_pos() 
 
        hover = self.rect.collidepoint(pos) 
 
        if hover: 
            self.glow()
            Menu.button_sound_on_select.play() 
            self.is_glowing = False 
        elif not self.is_glowing:
            self.screen.blit(self.image, (self.rect.x, self.rect.y)) 

        if self.rect.collidepoint(pos): 
            if pygame.mouse.get_pressed()[0] and not self.clicked: 
                self.clicked = True 
                action = True 
 
        if not pygame.mouse.get_pressed()[0]: 
            self.clicked = False 
 
        return action 
     
    @staticmethod 
    def buttons_init(screen: pygame.Surface) -> dict[str, "Menu"]: 
        buttons_dict = {} 
        #Buttons 
        start_button = pygame.image.load("materials/start_button.png").convert() 
        start_button.set_colorkey((0, 0, 0)) 
        start_button = pygame.transform.scale(start_button, (500, 200)) 
 
        HighScores_button = pygame.image.load("materials/HighScores_button.png").convert() 
        HighScores_button.set_colorkey((0, 0, 0)) 
        HighScores_button = pygame.transform.scale(HighScores_button, (500, 200)) 
 
        instruction_button = pygame.image.load("materials/instructions_button.png") 
        instruction_button.set_colorkey((0, 0, 0)) 
        instruction_button = pygame.transform.scale(instruction_button, (500, 200)) 
 
        exit_button = pygame.image.load("materials/exit_button.png").convert() 
        exit_button.set_colorkey((0, 0, 0)) 
        exit_button = pygame.transform.scale(exit_button, (500, 200)) 
 
        buttons_dict["start"] = Menu(start_button, 20, 0, screen) 
        buttons_dict["exit"] = Menu(exit_button, 20, 600, screen) 
        buttons_dict["HighScore"] = Menu(HighScores_button, 20, 200, screen) 
        buttons_dict["instruction"] = Menu(instruction_button, 20, 400, screen) 
 
        return buttons_dict 
 
    @staticmethod 
    def draw_menu(screen: pygame.Surface, selected: int, background: pygame.Surface, buttons_list: list["Menu"]) -> None: 
        screen.blit(background, (0, 0)) 
        if buttons_list[0].draw():
            Menu.button_sound_on_click.play() 
            print("start")
        if buttons_list[3].draw(): 
            Menu.button_sound_on_click.play()
            print("exit") 
        if buttons_list[1].draw(): 
            Menu.button_sound_on_click.play()
            print("HighScore")
        if buttons_list[2].draw():
            Menu.button_sound_on_click.play()
            print("Instructions") 
        buttons_list[selected].glow() 
        buttons_list[selected].is_glowing = False 
 
    @staticmethod
    def handle_event(event: pygame.event.Event, selected: int) -> int: 
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_DOWN: 
                selected = (selected + 1) % 4
                Menu.button_sound_on_select.play() 
            elif event.key == pygame.K_UP: 
                selected = (selected - 1) % 4
                Menu.button_sound_on_select.play()
            elif event.key == pygame.K_RETURN:
                Menu.button_sound_on_click.play() 
                print("Selected", selected) 
        return selected

    @staticmethod
    def menu_init(screen: pygame.Surface) -> tuple[pygame.Surface, list["Menu"]]:
        pygame.mixer.music.load("materials/pacman_menu_calm.wav")
        pygame.mixer.music.play(-1)
        background = pygame.image.load("materials/BackGround.png") 
        background = pygame.transform.scale(background, (1600, 900)) 
        
        buttons_dict = Menu.buttons_init(screen) 
        
        buttons_list = [ 
            buttons_dict["start"], 
            buttons_dict["HighScore"], 
            buttons_dict["instruction"], 
            buttons_dict["exit"] 
        ]
        return background, buttons_list