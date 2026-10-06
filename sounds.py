import pygame


pygame.mixer.init()
button_sound_on_select = pygame.mixer.Sound(
    "materials/pacman_button_select.wav")
button_sound_on_select.set_volume(0.7)
button_sound_on_click = pygame.mixer.Sound(
    "materials/pacman_button_click.wav")
