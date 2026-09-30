class Player:
    def __init__(self, position, lives):
        self.position = position
        self.lives = lives

    def move(self, direction, collision):
        if collision.can_move(self.position, direction):
            self.position = (
                self.position[0] + direction[0],
                self.position[1] + direction[1]
            )