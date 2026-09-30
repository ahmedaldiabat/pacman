class Game:
    def __init__(self, config):
        self.config = config
        self.player = pass
        self.ghosts = pass
        self.level = pass
        self.score = 0
        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self,keyboard_event: str):
        if keyboard_event == 'W':
            self.update(self.player, (0, 1))
        elif keyboard_event == 'A':
            self.update(self.player, (-1, 0))
        elif keyboard_event == 'S':
            self.update(self.player, (0, -1))
        elif keyboard_event == 'D':
            self.update(self.player, (1, 0))
        elif keyboard_event == "ESC":
            self.running = False
        elif keyboard_event == 'Q':
            self.running = False


    def update(self, direction):
        self.player.move(direction)

    def render(self):
        pass
