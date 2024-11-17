from enum import Enum, auto
from scripts.main_menu import run_main_menu
from scripts.manor import run_manor


class GameState(Enum):
    MAIN_MENU = auto()
    GAME = auto()


game_state: GameState = GameState.MAIN_MENU


def set_game_state(state: GameState):
    global game_state
    game_state = state


def run_game():
    """ Play a frame of the game
    """

    match game_state:
        case GameState.MAIN_MENU:
            run_main_menu()
        case GameState.GAME:
            run_manor()
        case _:
            raise ValueError("Invalid game state")
