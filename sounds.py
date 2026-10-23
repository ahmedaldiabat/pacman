"""Optional menu and gameplay sounds with graceful audio fallback."""
from __future__ import annotations

import pygame


def _load_sound(path: str, volume: float = 0.5):
    """Load a sound effect when the mixer and asset are available."""
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except (pygame.error, OSError):
        return None


def play(sound) -> None:
    """Play an optional sound without making audio a startup requirement."""
    if sound is not None:
        try:
            sound.play()
        except pygame.error:
            pass


button_sound_on_select = _load_sound("materials/pacman_button_select.wav", 0.45)
button_sound_on_click = _load_sound("materials/pacman_button_click.wav", 0.55)
pacgum_sound = _load_sound("materials/pacgum.wav", 0.38)
power_pellet_sound = _load_sound("materials/power_pellet.wav", 0.50)
ghost_eaten_sound = _load_sound("materials/ghost_eaten.wav", 0.58)
player_hit_sound = _load_sound("materials/player_hit.wav", 0.62)
