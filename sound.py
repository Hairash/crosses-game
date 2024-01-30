import os

import pygame

from const import BASE_PATH


def get_sound(path):
    return pygame.mixer.Sound(os.path.join(BASE_PATH, path))


def change_sound_volume(is_plus):
    volume = TURN_SOUND.get_volume()
    volume += 0.1 if is_plus else -0.1
    volume = max(0.0, min(volume, 1.0))
    volume = round(volume, 1)
    print('Sound volume:', volume)
    TURN_SOUND.set_volume(volume)
    CONGRATULATIONS_SOUND.set_volume(volume)


def change_music_volume(is_plus):
    volume = pygame.mixer.music.get_volume()
    volume += 0.1 if is_plus else -0.1
    volume = max(0.0, min(volume, 1.0))
    volume = round(volume, 1)
    print('Music volume:', volume)
    pygame.mixer.music.set_volume(volume)


pygame.mixer.init()

TURN_SOUNDS = {
    'Oak': get_sound('sound/Oak.mp3'),
    'Shuh': get_sound('sound/Shuh.mp3'),
    'Uaa': get_sound('sound/Uaa.mp3'),
    'Rm': get_sound('sound/Rm.mp3'),
}

TURN_SOUND = TURN_SOUNDS['Oak']
TURN_SOUND.set_volume(0.2)

CONGRATULATIONS_SOUNDS = {
    'Wooo': get_sound('sound/Wooo.mp3'),
    'Tududu': get_sound('sound/Tududu.mp3'),
}
CONGRATULATIONS_SOUND = CONGRATULATIONS_SOUNDS['Wooo']
CONGRATULATIONS_SOUND.set_volume(0.2)

pygame.mixer.music.load(os.path.join(BASE_PATH, 'sound/Croco theme.mp3'))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
