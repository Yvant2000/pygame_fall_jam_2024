from typing import Generator

from pygame import Surface

from scripts import input_manager, display, game
from scripts.coroutine_manager import create_coroutine
from scripts.display import get_delta_time
from scripts.objects.door import Door
from scripts.textures import ending_door


class EndingDoor(Door):
    def __init__(self):
        super().__init__((3.99, 0), False, (0, 0))
        self.image: Surface = ending_door
        self.buffer: Surface = self.image.copy()

    def interact(self):
        create_coroutine(end_game())


def end_game() -> Generator:
    input_manager.lock = True
    yield

    progress = 0
    while progress < 1:
        progress += get_delta_time()
        display.fade_black = progress
        yield

    game.game_state = game.GameState.END_SCREEN
    input_manager.lock = False

    progress = 0
    while progress < 1:
        progress += get_delta_time() / 3
        display.fade_black = 1 - progress
        yield

    display.fade_black = 0
