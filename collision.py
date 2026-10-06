class Collision:
    def __init__(self, maze):
        self.maze = maze

    def can_move(self, position, direction):
        x, y = position
        dx, dy = direction
        cell = self.maze[y][x]
        if dx == 1:
            return not (cell & 2)
        if dx == -1:
            return not (cell & 8)
        if dy == 1:
            return not (cell & 4)
        if dy == -1:
            return not (cell & 1)
        return False