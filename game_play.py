import pygame


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.cell_height = 1
        self.cell_width = 1

    def cellWalls(self, walls: int) -> list[int]:
        return [
            1 if walls & 1 else 0,
            1 if walls & 2 else 0,
            1 if walls & 4 else 0,
            1 if walls & 8 else 0
            ]

    def draw_gameplay(self, background, maze: list[list[int]]):
        self.screen.blit(background, (0, 0))
        pygame.draw.line(self.screen, (0, 80, 255), (250, 250), (250, 500), 10)
        for y in range(15):
            for x in range(15):
                cell = maze[y][x]
                print(cell)
        print(maze)
        exit()
