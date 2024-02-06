import os
import sys

# Path
BASE_PATH = os.path.dirname(sys.executable)
# Dev mode
if 'dev' in sys.argv:
    BASE_PATH = '.'

# Game parameters
INIT_ROWS = 1
WINDOW_SIZE = 600
INDENT_SIZE = 10
STEP_COUNTER_HEIGHT = 24
SAVE_FILE_PATH = '.progress.sav'


# Game consts
class CELL_VALUES:
    HORIZONTAL = 0
    VERTICAL = 1

# Buttons
SOUND_MINUS = 'sound_minus'
SOUND_PLUS = 'sound_plus'
MUSIC_MINUS = 'music_minus'
MUSIC_PLUS = 'music_plus'
