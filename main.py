from game import Game, EXIT_CODES

WINDOW_SIZE = 600


class GameCycle:
    def __init__(self):
        self.save_file_name = '.progress.sav'
        self.rows = 4
        self.difficulty_level = 1
        self.load_game()

    def load_game(self):
        try:
            with open(self.save_file_name, 'r') as f:
                self.rows, self.difficulty_level = list(map(int, f.readline().split(':')))
        except FileNotFoundError:
            pass

    def start(self):
        while True:
            if self.difficulty_level > self.rows * self.rows:
                self.rows += 1
                self.difficulty_level = 1
            self.save_game()
            game = Game(WINDOW_SIZE, self.rows, self.difficulty_level)
            exit_code = game.start()
            if exit_code == EXIT_CODES.QUIT:
                return
            self.difficulty_level += 1

    def save_game(self):
        with open(self.save_file_name, 'w') as f:
            f.write(f'{self.rows}:{self.difficulty_level}')


game_cycle = GameCycle()
game_cycle.start()
