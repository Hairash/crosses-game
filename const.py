import os
import sys

# Path
BASE_PATH = os.path.dirname(sys.executable)
# Dev mode
if 'dev' in sys.argv:
    BASE_PATH = '.'

# Game mode
class GAME_MODES:
    CHALLENGE = 'challenge'
    STORY = 'story'

GAME_MODE = GAME_MODES.CHALLENGE
if 'story' in sys.argv:
    GAME_MODE = GAME_MODES.STORY

# Game parameters
INIT_ROWS = 1
WINDOW_SIZE = 600
INDENT_SIZE = 10
STEP_COUNTER_HEIGHT = 30
SAVE_FILE_PATH = '.progress.sav'
if GAME_MODE == GAME_MODES.STORY:
    SAVE_FILE_PATH = '.story_progress.sav'


# Game consts
class CELL_VALUES:
    HORIZONTAL = 0
    VERTICAL = 1

# Buttons
SOUND_MINUS = 'sound_minus'
SOUND_PLUS = 'sound_plus'
MUSIC_MINUS = 'music_minus'
MUSIC_PLUS = 'music_plus'
