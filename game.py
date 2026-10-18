import pygame
from ghost import Ghost
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
            self.player_start_pos(),
            3,
            cell_size=self.renderer.gameplay.cell_size,
        )
        self.ghost = Ghost(
            pos=(1, 1),
            pixel_pos=pygame.Vector2(
                (1.5) * self.renderer.gameplay.cell_size,
                (1.5) * self.renderer.gameplay.cell_size
                ),
            current_dir=(0, 1),
            target_pos=None,
            target_cell=None,
            speed=100.0,
            collision=self.collision,
            cell_size=self.renderer.gameplay.cell_size,
        )
        self.init_gums()
        self.ghosts = []
        self.level = None
        self.score = 0
        self.running = True
        self.direction = None
        self.respawn_protection = 0.0

    def player_start_pos(self):
        maze_entry = self.maze_generator.maze_entry
        maze_exit = self.maze_generator.maze_exit
        x = (maze_entry[0] + maze_exit[0]) // 2
        y = (maze_entry[1] + maze_exit[1]) // 2
        while self.maze[y][x] == 15:
            x = x + 1
        if x >= self.maze_generator._width:
            x = (maze_entry[0] + maze_exit[0]) // 2
        while self.maze[y][x] == 15:
                    y = y + 1
        if y >= self.maze_generator._height:
            x = self.maze_generator._width // 2
            y = 0
        player_pos = (x, y)
        return player_pos
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
                self.renderer.render_gameplay(
                self.maze,
                self.player,
                self.gums,
                self.ghost,
            )
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
                    self.renderer.capture_pause_background()
                    self.renderer.state = "pause"
                elif self.renderer.state == "gameplay" and event.key in directions:
                    self.direction = directions[event.key]

            if self.renderer.state == "Menu":
                self.renderer.handle_menu_event(event)
            elif self.renderer.state == "Instruction":
                result = self.renderer.instruction.handle_event(event)
                if result == "back":
                    self.renderer.state = "Menu"

    
    
    def check_ghost_collision(self):
        if self.respawn_protection > 0:
            return
        distance = self.player.pixel_position.distance_to(
            self.ghost.pixel_position
        )

        if distance < self.player.cell_size * 0.6:
            self.player.lives -= 1
            self.respawn_protection = 1.5
            # Reset both characters to their starting positions.
            self.player.position = self.player_start_pos()
            self.player.pixel_position = pygame.Vector2(
                (self.player.position[0] + 0.5) * self.player.cell_size,
                (self.player.position[1] + 0.5) * self.player.cell_size,
            )
            self.player.target_position = None
            self.player.target_cell = None

            self.ghost.position = (1, 1)
            self.ghost.pixel_position = pygame.Vector2(
                (1.5) * self.ghost.cell_size,
                (1.5) * self.ghost.cell_size,
            )
            self.ghost.target_position = None
            self.ghost.target_cell = None

            if self.player.lives <= 0:
                self.renderer.state = "gameover"

    def update(self, dt: float):
        if self.renderer.state != "gameplay":
            return
        self.respawn_protection = max(
            0.0,
            self.respawn_protection - dt
            )

        position = self.player.update(
            self.direction,
            self.collision,
            dt,
            )

        if position is not None:
            x, y = position
            if self.gums[y][x] == 2:
                self.score += 50
                self.gums[y][x] = 0
            elif self.gums[y][x] == 1:
                self.score += 10
                self.gums[y][x] = 0

        self.ghost.update(dt, self.player.position)
        self.check_ghost_collision()


    def capture_pause_background(self):
        self.pause_background = self.screen.copy()

    def init_gums(self):
        height = self.maze_generator._height
        width = self.maze_generator._width

        self.gums = [[0] * width for _ in range(height)]

        start_x, start_y = self.player.position

        for y in range(height):
            for x in range(width):
                if self.maze[y][x] == 15:
                    self.gums[y][x] = 0
                elif (x, y) == (start_x, start_y):
                    self.gums[y][x] = 0
                elif y in (0, height - 1) and x in (0, width - 1):
                    self.gums[y][x] = 2
                else:
                    self.gums[y][x] = 1
