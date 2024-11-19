from enum import Enum, auto

from scripts.ending_screen import display_end_screen
from scripts.main_menu import run_main_menu
from scripts.manor import run_manor, init_manor


class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()
    END_SCREEN = auto()


game_state: GameState = GameState.MAIN_MENU


def start_game():  # Never ask what this function is for, I'm too ashamed
    global game_state
    game_state = GameState.GAME
    init_manor()


def run_game():
    """ Play a frame of the game
    """

    match game_state:
        case GameState.MAIN_MENU:
            run_main_menu()
        case GameState.GAME:
            run_manor()
        case GameState.END_SCREEN:
            display_end_screen()
        case _:
            raise ValueError("Invalid game state")
