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
        self.gums = []

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
                self.renderer.render_gameplay()

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

    def update(self):
        if self.direction is not None and self.player is not None:
            self.player.move(self.direction, self.collision)

    def init_gums(self):
        #here we use the 0 to represent that there is no gum
        #and we use the 1 to represent that there is a Pac-Gum
        #and we use the 2 to represent that there is a Super-Gum
        for i in self.maze_generator._width:
            for j in self.maze_generator._height:
                if self.maze[i][j] == 15:
                    self.gums[i][j] = 0
                elif i == 0 and j == 0:
                    self.gums[i][j] = 2
                elif i == 0 and self.maze_generator._height - 1:
                    self.gums[i][j] = 2
                elif i==self.maze_generator._width -1 and j == 0:
                    self.gums[i][j] = 2
                elif i==self.maze_generator._width -1 and j == self.maze_generator._height - 1:
                    self.gums[i][j] = 2
                else:
                    self.gums[i][j] = 1
