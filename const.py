import os
import sys

# Path
BASE_PATH = os.path.dirname(sys.executable)
# Dev mode
if len(sys.argv) > 1 and sys.argv[1] == 'dev':
    BASE_PATH = '.'

# Game parameters
INIT_ROWS = 1
WINDOW_SIZE = 600
INDENT_SIZE = 10
STEP_COUNTER_HEIGHT = 30
SAVE_FILE_PATH = '.progress.sav'


# Game consts
class CELL_VALUES:
    HORIZONTAL = 0
    VERTICAL = 1
