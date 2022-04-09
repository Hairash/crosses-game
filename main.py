from game import Game, EXIT_CODES

WINDOW_SIZE = 600

rows = 4
difficulty_level = 1
while True:
    if difficulty_level > rows * rows:
        rows += 1
        difficulty_level = 1
    game = Game(WINDOW_SIZE, rows, difficulty_level)
    exit_code = game.start()
    if exit_code == EXIT_CODES.QUIT:
        break
    difficulty_level += 1
