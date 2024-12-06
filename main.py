import os
from kivy.app import App
from kivy.resources import resource_find
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from const import WINDOW_SIZE, INIT_ROWS, SAVE_FILE_PATH, BASE_PATH
from game import Game, EXIT_CODES


class GameCycle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.save_file_name = os.path.join(BASE_PATH, SAVE_FILE_PATH)
        self.rows = INIT_ROWS
        self.difficulty_level = 1
        self.load_game()

    def load_game(self):
        """Load saved game state from file"""
        try:
            save_file_path = resource_find(self.save_file_name)
            with open(save_file_path, 'r') as f:
                self.rows, self.difficulty_level = list(map(int, f.readline().split(':')))
        except FileNotFoundError:
            pass

    def save_game(self):
        """Save the current game state to a file"""
        save_file_path = resource_find(self.save_file_name)
        with open(save_file_path, 'w') as f:
            f.write(f'{self.rows}:{self.difficulty_level}')

    def start_game(self):
        """Start the main game loop"""
        while True:
            if self.difficulty_level > self.rows * self.rows:
                self.rows += 1
                self.difficulty_level = 1
            self.save_game()

            # Replace Pygame game loop with Kivy event-based loop
            game = Game(self.rows, self.difficulty_level)
            exit_code = game.start()  # Placeholder for actual game logic

            if exit_code == EXIT_CODES.QUIT:
                return
            self.difficulty_level += 1


class MainMenu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.add_widget(Label(text="Welcome to Croco Game", font_size='20sp'))
        self.add_widget(Button(text="Start Game", on_press=self.start_game))
        self.add_widget(Button(text="Quit", on_press=self.quit_game))

    def start_game(self, instance):
        """Start the game"""
        game_cycle = GameCycle()
        game_cycle.start_game()

    def quit_game(self, instance):
        """Quit the application"""
        App.get_running_app().stop()


class CrocoGameApp(App):
    def build(self):
        """Build and return the root widget"""
        Window.size = (WINDOW_SIZE, WINDOW_SIZE)  # Set the game window size
        return MainMenu()


if __name__ == "__main__":
    CrocoGameApp().run()
