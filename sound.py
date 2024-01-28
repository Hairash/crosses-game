import os

import pygame

from const import BASE_PATH


def get_sound(path):
    return pygame.mixer.Sound(os.path.join(BASE_PATH, path))


pygame.mixer.init()

TURN_SOUNDS = {
    'Oak': get_sound('sound/Oak.mp3'),
    'Shuh': get_sound('sound/Shuh.mp3'),
    'Uaa': get_sound('sound/Uaa.mp3'),
    'Rm': get_sound('sound/Rm.mp3'),
}

TURN_SOUND = TURN_SOUNDS['Oak']
TURN_SOUND.set_volume(0.4)

CONGRATULATIONS_SOUNDS = {
    'Wooo': get_sound('sound/Wooo.mp3'),
    'Tududu': get_sound('sound/Tududu.mp3'),
}
CONGRATULATIONS_SOUND = CONGRATULATIONS_SOUNDS['Wooo']
CONGRATULATIONS_SOUND.set_volume(0.4)

pygame.mixer.music.load(os.path.join(BASE_PATH, 'sound/Croco theme.mp3'))
pygame.mixer.music.play(-1)
