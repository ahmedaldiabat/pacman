import pygame
import menu

pygame.init()
screen: pygame.Surface = pygame.display.set_mode((1600, 900))

selected = 0
pygame.display.set_caption("PacMan")
clock = pygame.time.Clock()

run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        selected = menu.Menu.handle_event(event, selected)
    
    
    menu.Menu.draw_menu(screen, selected)


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
