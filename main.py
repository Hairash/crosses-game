from game import Game, EXIT_CODES

N = 4
WINDOW_SIZE = 600
STEPS = 1

while True:
    game = Game(WINDOW_SIZE, N, STEPS)
    exit_code = game.start()
    if exit_code == EXIT_CODES.QUIT:
        break
