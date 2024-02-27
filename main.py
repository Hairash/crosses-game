import os
import sys

import pygame

from game_story import GameStory
from story import DIFFICULTY_LEVEL_STEPS
pygame.init()

from const import GAME_MODE, GAME_MODES, INIT_ROWS, SAVE_FILE_PATH, BASE_PATH
from game import Game, EXIT_CODES


print('BASE PATH:', BASE_PATH)


class GameCycle:
    def __init__(self):
        self.save_file_name = os.path.join(BASE_PATH, SAVE_FILE_PATH)
        self.rows = INIT_ROWS
        self.mask_level = 1
        self.difficulty_level = 1
        self.load_game()
        self.mask = []
        if GAME_MODE == GAME_MODES.STORY:
            self.get_mask()

    def load_game(self):
        try:
            with open(self.save_file_name, 'r') as f:
                if GAME_MODE == GAME_MODES.CHALLENGE:
                    self.rows, self.difficulty_level = list(map(int, f.readline().split(':')))
                else:
                    mask_str, difficulty_level_str = f.readline().split(':')
                    self.difficulty_level = int(difficulty_level_str)
                    self.rows, self.mask_level = [int(x) for x in mask_str.split('-')]
        except FileNotFoundError:
            pass

    def get_mask(self):
        with open(f'levels/{self.rows}-{self.mask_level}.lvl', 'r') as f:
            mask = [[int(num) for num in line.split()] for line in f if line.strip()]
            # Traspose mask
            self.mask = [list(x) for x in list(zip(*mask))]


    def start(self):
        while True:
            self.check_and_process_level_up()
            self.save_game()
            if GAME_MODE == GAME_MODES.STORY:
                game = GameStory(self.rows, self.difficulty_level, self.mask)
            else:
                game = Game(self.rows, self.difficulty_level)
            exit_code = game.start()
            if exit_code == EXIT_CODES.QUIT:
                return
            self.calculate_next_difficulty_level()

    def calculate_next_difficulty_level(self):
        if GAME_MODE == GAME_MODES.CHALLENGE:
            self.difficulty_level += 1
            return
        steps = DIFFICULTY_LEVEL_STEPS[self.rows][self.mask_level]
        if type(steps) == int:
            self.difficulty_level += steps
            return
        try:
            self.difficulty_level = steps[steps.index(self.difficulty_level) + 1]
        except IndexError:
            self.difficulty_level = float('inf')

    def check_and_process_level_up(self):
        if GAME_MODE == GAME_MODES.CHALLENGE:
            if self.difficulty_level > self.rows * self.rows:
                self.rows += 1
                self.difficulty_level = 1
        else:
            if self.difficulty_level > sum([sum(x) for x in self.mask]):
                self.mask_level += 1
                try:
                    self.get_mask()
                except FileNotFoundError:
                    # All masks for current stage completed
                    self.rows +=1
                    self.mask_level = 1
                    try:
                        self.get_mask()
                    # No more levels - end of game
                    except FileNotFoundError:
                        self.rows = 0
                self.difficulty_level = 1

    def save_game(self):
        with open(self.save_file_name, 'w') as f:
            if GAME_MODE == GAME_MODES.CHALLENGE:
                f.write(f'{self.rows}:{self.difficulty_level}')
            else:
                f.write(f'{self.rows}-{self.mask_level}:{self.difficulty_level}')


game_cycle = GameCycle()
game_cycle.start()
