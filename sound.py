import pygame

pygame.mixer.init()

TURN_SOUNDS = {
    'Oak': pygame.mixer.Sound('sound/Oak.mp3'),
    'Shuh': pygame.mixer.Sound('sound/Shuh.mp3'),
    'Uaa': pygame.mixer.Sound('sound/Uaa.mp3'),
    'Rm': pygame.mixer.Sound('sound/Rm.mp3'),
}

TURN_SOUND = TURN_SOUNDS['Oak']
TURN_SOUND.set_volume(0.4)

CONGRATULATIONS_SOUNDS = {
    'Wooo': pygame.mixer.Sound('sound/Wooo.mp3'),
    'Tududu': pygame.mixer.Sound('sound/Tududu.mp3'),
}
CONGRATULATIONS_SOUND = CONGRATULATIONS_SOUNDS['Wooo']
CONGRATULATIONS_SOUND.set_volume(0.4)

pygame.mixer.music.load('sound/Croco theme.mp3')
pygame.mixer.music.play(-1)
