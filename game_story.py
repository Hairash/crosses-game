"""Naming rules
x, y - mouse coordinates (px)
cell_x, cell_y - cell coordinates (0..N-1)
"""

import pygame
import random
import typing
from button import Button

from const import (
    CELL_VALUES,
    MUSIC_MINUS,
    MUSIC_PLUS,
    SOUND_MINUS,
    SOUND_PLUS,
    WINDOW_SIZE,
    INDENT_SIZE,
)

from graphics import (
    MINUS_BUTTON,
    PLUS_BUTTON,
    WINDOW,
    BACKGROUND,
    BACKGROUND_IMAGE,
    WIN_LABEL,
    STEP_COUNTER,
    DIGIT_IMAGE,
    get_cell_values_images,
    # fade_out,
    # grow_image,
)
from sound import (
    TURN_SOUND,
    CONGRATULATIONS_SOUND,
    change_sound_volume,
    change_music_volume,
)


class EXIT_CODES:
    QUIT = 0
    NEW = 1


class GameStory:
    def __init__(self, rows: int, difficulty_level: int, mask: list[list[int]]):
        self.window_size = WINDOW_SIZE
        self.rows = rows
        self.difficulty_level = difficulty_level
        self.mask = mask
        if self.rows:
            self.check_mask()
            self.cell_size = self.window_size // self.rows
            self.images = get_cell_values_images(self.cell_size)
        self.window = WINDOW
        self.buttons = {
            SOUND_MINUS: None,
            SOUND_PLUS: None,
            MUSIC_MINUS: None,
            MUSIC_PLUS: None,
        }

        self.field = [[CELL_VALUES.HORIZONTAL] * self.rows for _ in range(self.rows)]
        self.cur_step = 0

    def check_mask(self):
        if len(self.mask) != self.rows or len(self.mask[0]) != self.rows:
            raise Exception('Wrong mask')

    def start(self):
        pygame.display.set_caption(f'Croco game. Level: {self.difficulty_level}')
        self.shuffle(self.difficulty_level)
        self.draw_field()

        if not self.rows:
            self.end_game()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return EXIT_CODES.QUIT
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.is_end_game():
                            return EXIT_CODES.NEW
                        mouse_pos = pygame.mouse.get_pos()
                        self.process_buttons(mouse_pos)
                        self.change_cell_cross_by_mouse(mouse_pos)
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

    def change_cell_cross_by_mouse(self, mouse_pos):
        cur_cell_x, cur_cell_y = self.coordinates_to_cell(*mouse_pos)
        if self.are_cell_coords_correct(cur_cell_x, cur_cell_y) and self.is_in_mask(cur_cell_x, cur_cell_y):
            self.change_cell_cross(cur_cell_x, cur_cell_y)
            self.increase_step()
            pygame.mixer.Sound.play(TURN_SOUND)

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

    def process_buttons(self, mouse_pos):
        if self.buttons[SOUND_MINUS].is_over(mouse_pos):
            change_sound_volume(False)
        if self.buttons[SOUND_PLUS].is_over(mouse_pos):
            change_sound_volume(True)
        if self.buttons[MUSIC_MINUS].is_over(mouse_pos):
            change_music_volume(False)
        if self.buttons[MUSIC_PLUS].is_over(mouse_pos):
            change_music_volume(True)

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

    def draw_buttons(self):
        self.buttons[SOUND_MINUS] = Button(
            self.window,
            INDENT_SIZE,
            INDENT_SIZE,
            MINUS_BUTTON.width,
            MINUS_BUTTON.height,
            MINUS_BUTTON.image,
        )
        self.buttons[SOUND_MINUS].draw()

        self.buttons[SOUND_PLUS] = Button(
            self.window,
            INDENT_SIZE + MINUS_BUTTON.width * 2,
            INDENT_SIZE,
            PLUS_BUTTON.width,
            PLUS_BUTTON.height,
            PLUS_BUTTON.image,
        )
        self.buttons[SOUND_PLUS].draw()

        self.buttons[MUSIC_MINUS] = Button(
            self.window,
            INDENT_SIZE + MINUS_BUTTON.width * 6,
            INDENT_SIZE,
            MINUS_BUTTON.width,
            MINUS_BUTTON.height,
            MINUS_BUTTON.image,
        )
        self.buttons[MUSIC_MINUS].draw()

        self.buttons[MUSIC_PLUS] = Button(
            self.window,
            INDENT_SIZE + MINUS_BUTTON.width * 8,
            INDENT_SIZE,
            PLUS_BUTTON.width,
            PLUS_BUTTON.height,
            PLUS_BUTTON.image,
        )
        self.buttons[MUSIC_PLUS].draw()

    def draw_background(self):
        self.window.blit(BACKGROUND_IMAGE, (0, 0))

    def draw_field(self):
        """Draw everything in the correct order"""
        pygame.draw.rect(self.window, BACKGROUND, (
            0, 0, self.window_size + 2 * INDENT_SIZE, self.window_size + 2 * INDENT_SIZE + STEP_COUNTER.height
        ))
        self.draw_background()
        self.draw_step_counter()
        self.draw_buttons()
        for cell_x in range(self.rows):
            for cell_y in range(len(self.field[cell_x])):
                if self.is_in_mask(cell_x, cell_y):
                    self.fill_cell(cell_x, cell_y)

    def is_in_mask(self, cell_x, cell_y):
        return self.mask[cell_x][cell_y] == 1

    def shuffle(self, steps: int):
        # Check that the result is not solved yet
        # print('Shuffle')
        while self.field == [[0] * self.rows] * self.rows:
            cell_set = set()
            for _ in range(steps):
                cell_x = random.randint(0, self.rows - 1)
                cell_y = random.randint(0, self.rows - 1)
                while (cell_x, cell_y) in cell_set or not self.is_in_mask(cell_x, cell_y):
                    cell_x = random.randint(0, self.rows - 1)
                    cell_y = random.randint(0, self.rows - 1)
                # print(cell_x, cell_y)
                self.change_cell_cross(cell_x, cell_y)
                cell_set.add((cell_x, cell_y))

    def is_end_game(self) -> bool:
        for cell_x in range(self.rows):
            for cell_y in range(self.rows):
                if self.is_in_mask(cell_x, cell_y) and self.field[cell_x][cell_y] == CELL_VALUES.VERTICAL:
                    return False
        return True

    def draw_win_label(self):
        x = int((self.window_size + 2 * INDENT_SIZE - WIN_LABEL.width) / 2)
        # Custom label output on the first odd levels
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

    def end_game(self):
        self.draw_win_label()
