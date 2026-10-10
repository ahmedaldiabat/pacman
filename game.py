import pygame
from mazegenerator import MazeGenerator
from player import Player
from collision import Collision


class Game:
    def __init__(self, config, renderer):
        self.config = config
        self.maze_generator = MazeGenerator(
            size=(15, 15),
            perfect=False,
            seed=42
            )
        self.maze = self.maze_generator.maze
        self.collision = Collision(self.maze)
        self.player = Player(
            self.maze_generator.maze_entry,
            3
            )
        self.ghosts = []
        self.level = None
        self.renderer = renderer
        self.score = 0
        self.running = True
        self.direction = None

    def run(self):
        while self.running:
            events = self.renderer.get_events()
            self.handle_events(events)
            self.update()
            if self.renderer.state == "Menu":
                self.renderer.render_menu()
            elif self.renderer.state == "Instruction":
                self.renderer.render_instruction()
            if self.renderer.state == "gameplay":
                self.renderer.render_gameplay(self.maze)

        self.renderer.quit()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.direction = (0, 1)
                elif event.key == pygame.K_a:
                    self.direction = (-1, 0)
                elif event.key == pygame.K_s:
                    self.direction = (0, -1)
                elif event.key == pygame.K_d:
                    self.direction = (1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            if self.renderer.state == "Menu":
                self.renderer.handle_menu_event(event)
            elif self.renderer.state == "Instruction":
                temp = self.renderer.instruction.handle_event(event)
                if temp == "back":
                    self.renderer.state = "Menu"
    def update(self):
        if self.direction is not None and self.player is not None:
            self.player.move(self.direction, self.collision)
