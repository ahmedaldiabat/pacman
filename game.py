import pygame
from mazegenerator import MazeGenerator
from player import Player
from collision import Collision


class Game:
    def __init__(self, config, renderer):
        self.config = config
        self.renderer = renderer
        self.maze_generator = MazeGenerator(
            size=(15, 15),
            perfect=False,
            seed=42,
        )
        self.maze = self.maze_generator.maze
        self.collision = Collision(self.maze)
        self.player = Player(
            self.maze_generator.maze_entry,
            3,
            cell_size=self.renderer.gameplay.cell_size,
        )
        self.ghosts = []
        self.level = None
        self.score = 0
        self.running = True
        self.direction = None

    def run(self):
        while self.running:
            # Use one shared frame limiter for every screen/state.
            dt = min(self.renderer.clock.tick(60) / 1000.0, 0.05)
            events = self.renderer.get_events()
            self.handle_events(events)
            self.update(dt)

            if self.renderer.state == "Menu":
                self.renderer.render_menu()
            elif self.renderer.state == "Instruction":
                self.renderer.render_instruction()
            elif self.renderer.state == "gameplay":
                self.renderer.render_gameplay(self.maze, self.player)
            elif self.renderer.state == "pause":
                self.renderer.render_pause()

        self.renderer.quit()

    def handle_events(self, events):
        directions = {
            pygame.K_w: (0, -1),
            pygame.K_UP: (0, -1),
            pygame.K_s: (0, 1),
            pygame.K_DOWN: (0, 1),
            pygame.K_a: (-1, 0),
            pygame.K_LEFT: (-1, 0),
            pygame.K_d: (1, 0),
            pygame.K_RIGHT: (1, 0),
        }

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.renderer.state == "Menu":
                    self.running = False
                elif event.key == pygame.K_ESCAPE and self.renderer.state == "Instruction":
                    self.renderer.state = "Menu"
                elif event.key == pygame.K_ESCAPE and self.renderer.state == "gameplay":
                    self.renderer.state = "pause"
                elif self.renderer.state == "gameplay" and event.key in directions:
                    self.direction = directions[event.key]

            if self.renderer.state == "Menu":
                self.renderer.handle_menu_event(event)
            elif self.renderer.state == "Instruction":
                result = self.renderer.instruction.handle_event(event)
                if result == "back":
                    self.renderer.state = "Menu"

    def update(self, dt: float):
        if self.renderer.state == "gameplay" and self.player is not None:
            self.player.update(self.direction, self.collision, dt)
