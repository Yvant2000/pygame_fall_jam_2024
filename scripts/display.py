from typing import Final

from pygame import display, transform, Surface, Clock
from pygame.constants import FULLSCREEN, SCALED, SRCALPHA

from scripts.config import window_size, game_screen_size, fps

window: Surface
window_top_layer: Surface
game_screen: Surface

clock: Final[Clock] = Clock()
delta_time: float = 0  # seconds

display_ratio: float = 0.8  # how bug is the game screen compared to the window. 1.0 is the max value


def init_display():
    """Initialize the display for the game. \n
    This function should be called before any other display functions.
    """
    global window, game_screen, window_top_layer
    window = display.set_mode(window_size, FULLSCREEN | SCALED, vsync=True)
    window_top_layer = Surface(window_size, SRCALPHA).convert_alpha()
    game_screen = Surface(game_screen_size)


def update_display():
    """Update the display with the game screen."""

    assert window is not None and game_screen is not None, "Display not initialized."

    window_width, window_height = window_size
    width, height = game_screen_size
    resized_height: int = round(window_height * display_ratio)
    resized_width: int = width * resized_height // height

    resized_game_screen: Surface = transform.scale(game_screen, (resized_width, resized_height))

    pos_x = (window_width - resized_width) // 2
    pos_y = (window_height - resized_height) // 2

    window.blit(resized_game_screen, (pos_x, pos_y))
    window.blit(window_top_layer, (0, 0))

    display.flip()


def clear_game_screen():
    """Clear the game screen."""
    global delta_time

    assert game_screen is not None, "Display not initialized."
    game_screen.fill((0, 0, 0))
    window.fill((0, 0, 0))
    window_top_layer.fill((0, 0, 0, 0))

    delta_time = clock.tick(fps) / 1000


def get_delta_time() -> float:
    """Get the time in seconds since the last frame. Usually, it's a small number like 0.016."""
    return delta_time
