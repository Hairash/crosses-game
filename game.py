"""Naming rules
x, y - mouse coordinates (px)
cell_x, cell_y - cell coordinates (0..N-1)
"""

import pygame
import random

pygame.font.init()
GRAY = (218, 218, 218)
BLACK = (0, 0, 0)


class WIN_LABEL:
    text = 'Congratulations!'
    font = pygame.font.SysFont('Comic Sans', 48)
    width = 275
    height = 40


class CELL_VALUES:
    SERVICE = -2
    EMPTY = -1
    HORIZONTAL = 0
    VERTICAL = 1


CELL_VALUE_IMAGE_DICT = {
    CELL_VALUES.SERVICE: 'images/black.png',
    CELL_VALUES.EMPTY: 'images/white.png',
    CELL_VALUES.HORIZONTAL: 'images/b_horizontal.png',
    CELL_VALUES.VERTICAL: 'images/b_vertical.png',
}


def get_cell_values_images(cell_size):
    return {
        key: pygame.transform.scale(pygame.image.load(value), (cell_size, cell_size))
        for key, value in CELL_VALUE_IMAGE_DICT.items()
    }


class Game:
    def __init__(self, window_size, rows, steps):
        self.window_size = window_size
        self.rows = rows
        self.steps = steps
        self.cell_size = self.window_size // self.rows
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        self.images = get_cell_values_images(self.cell_size)

        self.field = [[CELL_VALUES.HORIZONTAL] * self.rows for _ in range(self.rows)]
        # self.is_end_game = False

    def start(self):
        pygame.init()
        pygame.display.set_caption('Crosses')

        self.draw_field()
        self.shuffle(self.steps)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.is_end_game():
                    if event.button == 1:
                        self.change_cell_cross_by_mouse()
                        if self.is_end_game():
                            self.draw_win_label()
            pygame.display.update()

    def change_cell_cross_by_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        cur_cell_x, cur_cell_y = self.coordinates_to_cell(*mouse_pos)
        self.change_cell_cross(cur_cell_x, cur_cell_y)

    def change_cell_cross(self, cur_cell_x, cur_cell_y):
        for cell_x in range(0, len(self.field)):
            if cell_x == cur_cell_x:
                continue
            self.toggle_cell(cell_x, cur_cell_y)
        for cell_y in range(0, len(self.field)):
            if cell_y == cur_cell_y:
                continue
            self.toggle_cell(cur_cell_x, cell_y)
        self.toggle_cell(cur_cell_x, cur_cell_y)

    def toggle_cell(self, cell_x, cell_y):
        value = self.field[cell_x][cell_y]
        self.field[cell_x][cell_y] = (value + 1) % 2
        self.fill_cell(cell_x, cell_y)

    def coordinates_to_cell(self, x, y):
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        return cell_x, cell_y

    def cell_image_coordinates(self, cell_x, cell_y):
        x = self.cell_size * cell_x
        y = self.cell_size * cell_y
        return x, y

    def fill_cell(self, cell_x, cell_y):
        x, y = self.cell_image_coordinates(cell_x, cell_y)
        value = self.field[cell_x][cell_y]
        # TODO: May be done better
        self.window.blit(self.images[CELL_VALUES.EMPTY], (x, y))
        self.window.blit(self.images[value], (x, y))

    def draw_field(self):
        for x in range(len(self.field)):
            for y in range(len(self.field[x])):
                self.fill_cell(x, y)

    def shuffle(self, steps):
        for _ in range(steps):
            cell_x = random.randint(0, len(self.field) - 1)
            cell_y = random.randint(0, len(self.field) - 1)
            self.change_cell_cross(cell_x, cell_y)

    def is_end_game(self):
        for row in self.field:
            for cell in row:
                if cell == CELL_VALUES.VERTICAL:
                    return False
        return True

    # def check_end_game(self):
    #     if self._is_end_game():
    #         self.is_end_game = True

    def draw_win_label(self):
        x = int((self.window_size - WIN_LABEL.width) / 2)
        y = int((self.window_size - WIN_LABEL.height) / 2)
        text_img = WIN_LABEL.font.render(WIN_LABEL.text, True, BLACK)
        self.window.blit(text_img, (x, y))
