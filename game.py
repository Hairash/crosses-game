"""Naming rules
x, y - mouse coordinates (px)
cell_x, cell_y - cell coordinates (0..N-1)
"""

import pygame
import random
import typing

from const import CELL_VALUES, WINDOW_SIZE, INDENT_SIZE

from graphics import (
    WINDOW,
    BACKGROUND,
    BACKGROUND_IMAGE,
    WIN_LABEL,
    STEP_COUNTER,
    DIGIT_IMAGE,
    get_cell_values_images,
    fade_out, grow_image,
)
from sound import TURN_SOUND, CONGRATULATIONS_SOUND


class EXIT_CODES:
    QUIT = 0
    NEW = 1


class Game:
    def __init__(self, rows: int, difficulty_level: int):
        if difficulty_level > rows * rows:
            raise Exception('Difficulty level cannot be so high')
        self.window_size = WINDOW_SIZE
        self.rows = rows
        self.difficulty_level = difficulty_level
        self.cell_size = self.window_size // self.rows
        self.window = WINDOW
        self.images = get_cell_values_images(self.cell_size)

        self.field = [[CELL_VALUES.HORIZONTAL] * self.rows for _ in range(self.rows)]
        self.cur_step = 0

    def start(self):
        pygame.display.set_caption(f'Croco game. Level: {self.difficulty_level}')
        self.shuffle(self.difficulty_level)
        self.draw_field()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return EXIT_CODES.QUIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.is_end_game():
                            return EXIT_CODES.NEW
                        pygame.mixer.Sound.play(TURN_SOUND)
                        self.change_cell_cross_by_mouse()
                        self.draw_field()
                        if self.is_end_game():
                            self.draw_win_label()
                            pygame.mixer.Sound.stop(TURN_SOUND)
                            pygame.mixer.Sound.play(CONGRATULATIONS_SOUND)

            pygame.display.update()

    def increase_step(self):
        self.cur_step += 1

    def are_cell_coords_correct(self, cell_x, cell_y):
        return 0 <= cell_x < self.rows and 0 <= cell_y < self.rows

    def change_cell_cross_by_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        cur_cell_x, cur_cell_y = self.coordinates_to_cell(*mouse_pos)
        if self.are_cell_coords_correct(cur_cell_x, cur_cell_y):
            self.change_cell_cross(cur_cell_x, cur_cell_y)
            self.increase_step()

    def change_cell_cross(self, cur_cell_x: int, cur_cell_y: int):
        for cell_x in range(0, self.rows):
            if cell_x == cur_cell_x:
                continue
            self.toggle_cell(cell_x, cur_cell_y)
        for cell_y in range(0, self.rows):
            if cell_y == cur_cell_y:
                continue
            self.toggle_cell(cur_cell_x, cell_y)
        self.toggle_cell(cur_cell_x, cur_cell_y)

    def toggle_cell(self, cell_x: int, cell_y: int):
        value = self.field[cell_x][cell_y]
        self.field[cell_x][cell_y] = (value + 1) % 2

    def coordinates_to_cell(self, x: int, y: int) -> (int, int):
        cell_x = (x - INDENT_SIZE) // self.cell_size
        cell_y = (y - INDENT_SIZE - STEP_COUNTER.height) // self.cell_size
        return cell_x, cell_y

    def cell_image_coordinates(self, cell_x: int, cell_y: int) -> (int, int):
        x = self.cell_size * cell_x + INDENT_SIZE
        y = self.cell_size * cell_y + INDENT_SIZE + STEP_COUNTER.height
        return x, y

    def fill_cell(self, cell_x: int, cell_y: int):
        x, y = self.cell_image_coordinates(cell_x, cell_y)
        value = self.field[cell_x][cell_y]
        self.window.blit(self.images[value], (x, y))

    @staticmethod
    def _get_digit_list(num: int) -> typing.List[int]:
        if num == 0:
            return [0]

        digits = []
        while num > 0:
            digits.append(num % 10)
            num //= 10
        return digits[::-1]

    def _draw_digit(self, digit: int, digit_offset: int, step_counter_right_offset: int):
        x = self.window_size + INDENT_SIZE - step_counter_right_offset + digit_offset
        y = INDENT_SIZE
        self.window.blit(DIGIT_IMAGE.images[digit], (x, y))

    def draw_step_counter(self):
        digit_list = self._get_digit_list(self.cur_step)
        step_counter_right_offset = DIGIT_IMAGE.width * len(digit_list)
        x = self.window_size - STEP_COUNTER.width - step_counter_right_offset
        y = INDENT_SIZE
        self.window.blit(STEP_COUNTER.image, (x, y))

        for i, digit in enumerate(digit_list):
            self._draw_digit(digit, i * DIGIT_IMAGE.width, step_counter_right_offset)

    def draw_background(self):
        self.window.blit(BACKGROUND_IMAGE, (0, 0))

    def draw_field(self):
        """Draw everything in the correct order"""
        pygame.draw.rect(self.window, BACKGROUND, (
            0, 0, self.window_size + 2 * INDENT_SIZE, self.window_size + 2 * INDENT_SIZE + STEP_COUNTER.height
        ))
        self.draw_background()
        self.draw_step_counter()
        for x in range(self.rows):
            for y in range(len(self.field[x])):
                self.fill_cell(x, y)

    def shuffle(self, steps: int):
        while self.field == [[0] * self.rows] * self.rows:
            cell_set = set()
            for _ in range(steps):
                cell_x = random.randint(0, self.rows - 1)
                cell_y = random.randint(0, self.rows - 1)
                while (cell_x, cell_y) in cell_set:
                    cell_x = random.randint(0, self.rows - 1)
                    cell_y = random.randint(0, self.rows - 1)
                self.change_cell_cross(cell_x, cell_y)
                cell_set.add((cell_x, cell_y))

    def is_end_game(self) -> bool:
        for row in self.field:
            for cell in row:
                if cell == CELL_VALUES.VERTICAL:
                    return False
        return True

    def draw_win_label(self):
        x = int((self.window_size + 2 * INDENT_SIZE - WIN_LABEL.width) / 2)
        # Custom label output on the first level only
        if self.rows == 1:
            y = int(self.window_size * 0.4 + STEP_COUNTER.height)
        elif self.rows == 3:
            y = int(-self.window_size * 0.16 + STEP_COUNTER.height)
        elif self.rows == 5:
            y = int(-self.window_size * 0.08 + STEP_COUNTER.height)
        else:
            y = int((self.window_size - WIN_LABEL.height) / 2) + STEP_COUNTER.height + INDENT_SIZE
        # print(x, y)
        # fade_out(self.window, 2)  # fade out over 2 seconds
        # grow_image(self.window, WIN_LABEL.image, (x, y), 0.5)  # fade out over 2 seconds

        if self.rows >= 11:
            num_lines_to_fill = self.rows // 5
            num_lines_to_fill = (num_lines_to_fill + (self.rows + 1) % 2) // 2 * 2 + self.rows % 2
            pygame.draw.rect(self.window, BACKGROUND, (
                0,
                (self.rows - num_lines_to_fill) // 2 * self.cell_size + INDENT_SIZE + STEP_COUNTER.height,
                self.window_size + 2 * INDENT_SIZE,
                self.cell_size * num_lines_to_fill,
            ))
        elif self.rows >= 7 and self.rows % 2:
            pygame.draw.rect(self.window, BACKGROUND, (
                0,
                (self.rows - 1) // 2 * self.cell_size + INDENT_SIZE + STEP_COUNTER.height,
                self.window_size + 2 * INDENT_SIZE,
                self.cell_size,
            ))
        elif self.rows >= 8 and not self.rows % 2:
            pygame.draw.rect(self.window, BACKGROUND, (
                0,
                (self.rows // 2 - 1) * self.cell_size + INDENT_SIZE + STEP_COUNTER.height,
                self.window_size + 2 * INDENT_SIZE,
                self.cell_size * 2,
            ))
        self.window.blit(WIN_LABEL.image, (x, y))
