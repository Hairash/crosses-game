import os

import pygame

from const import WINDOW_SIZE, INDENT_SIZE, CELL_VALUES, STEP_COUNTER_HEIGHT, BASE_PATH

pygame.init()
icon = pygame.image.load(os.path.join(BASE_PATH, 'images/croc_left.png'))
pygame.display.set_icon(icon)
pygame.font.init()
WINDOW = pygame.display.set_mode(
    (WINDOW_SIZE + 2 * INDENT_SIZE, WINDOW_SIZE + 2 * INDENT_SIZE + STEP_COUNTER_HEIGHT),
)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND = (0, 33, 36)


# Images
def get_pygame_image(path, width, height):
    return pygame.transform.scale(pygame.image.load(os.path.join(BASE_PATH, path)), (width, height))


class WIN_LABEL:
    width = 600
    height = 600
    image = get_pygame_image('images/labels/true_crocodile.png', width, height)
    image = image.convert_alpha()
    label_height = 51


class STEP_COUNTER:
    width = 105
    height = STEP_COUNTER_HEIGHT
    image = get_pygame_image('images/labels/steps.png', width, height)


class DIGIT_IMAGE:
    width = 23
    height = STEP_COUNTER_HEIGHT
    DIGIT_IMAGE_DICT = {
        0: 'images/digits/0.png',
        1: 'images/digits/1.png',
        2: 'images/digits/2.png',
        3: 'images/digits/3.png',
        4: 'images/digits/4.png',
        5: 'images/digits/5.png',
        6: 'images/digits/6.png',
        7: 'images/digits/7.png',
        8: 'images/digits/8.png',
        9: 'images/digits/9.png',
    }
    images = {}
    for key, value in DIGIT_IMAGE_DICT.items():
        images[key] = get_pygame_image(value, width, height)

class MINUS_BUTTON:
    width = STEP_COUNTER_HEIGHT
    height = STEP_COUNTER_HEIGHT
    image = get_pygame_image('images/labels/minus.png', width, height)


class PLUS_BUTTON:
    width = STEP_COUNTER_HEIGHT
    height = STEP_COUNTER_HEIGHT
    image = get_pygame_image('images/labels/plus.png', width, height)


CELL_VALUE_IMAGE_DICT = {
    CELL_VALUES.HORIZONTAL: 'images/croc_left.png',
    CELL_VALUES.VERTICAL: 'images/croc_up.png',
}


def get_cell_values_images(cell_size):
    return {
        key: get_pygame_image(value, cell_size, cell_size)
        for key, value in CELL_VALUE_IMAGE_DICT.items()
    }


BACKGROUND_IMAGE = get_pygame_image(
    'images/background.png',
    WINDOW_SIZE + 2 * INDENT_SIZE + STEP_COUNTER.height,
    WINDOW_SIZE + 2 * INDENT_SIZE + STEP_COUNTER.height,
)


def fade_out(window, duration):
    clock = pygame.time.Clock()
    alpha_surface = pygame.Surface(window.get_size())  # fullscreen surface
    alpha = 0
    while alpha <= 60:
        alpha_surface.set_alpha(alpha)
        window.blit(alpha_surface, (0, 0))  # cover the entire screen with the surface
        pygame.display.update()
        alpha += 255 / (duration * 60)  # increase alpha slowly over 'duration' seconds
        clock.tick(60)  # limit the while loop to 60 iterations per second (60FPS)


def grow_image(window, image, pos, duration):
    clock = pygame.time.Clock()
    original_image = image.copy()  # copy of the original image
    width, height = image.get_size()
    start_time = pygame.time.get_ticks()
    while True:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time > duration:
            break

        # Calculate the scale factor
        scale_factor = elapsed_time / duration
        new_size = (int(width * scale_factor), int(height * scale_factor))

        # Clear the window
        window.fill((0, 0, 0))

        # Scale the image and draw it
        scaled_image = pygame.transform.scale(original_image, new_size)
        window.blit(scaled_image, pos)

        pygame.display.update()
        clock.tick(60)
