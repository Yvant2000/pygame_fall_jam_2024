from typing import Final

from pygame import display, transform, Surface, Clock
from pygame.constants import SRCALPHA, BLEND_RGB_SUB

window_size: tuple[int, int]
overlay_size: tuple[int, int]
game_screen_size: Final[tuple[int, int]] = 64, 64

window: Surface
window_top_layer: Surface
game_screen: Surface

clock: Final[Clock] = Clock()
delta_time: float = 0  # seconds

display_ratio: float = 0.8  # how bug is the game screen compared to the window. value between 0 and 1
display_flat: float = 0.0  # how much the game screen is flat. value between 0 and 1
display_rotate: float = 0.0
fps: Final[int] = 60
fade_black: float = 0.0  # how much the screen is black. value between 0 and 1


def init_display():
    """Initialize the display for the game. \n
    This function should be called before any other display functions.
    """
    global window, game_screen, window_top_layer, window_size, overlay_size
    window = display.set_mode(vsync=True)
    window_size = window.get_size()
    overlay_size = window_size[0] * 1080 // window_size[1], 1080
    window_top_layer = Surface(overlay_size, SRCALPHA).convert_alpha()
    game_screen = Surface(game_screen_size)


def update_display():
    """Update the display with the game screen."""

    assert window is not None and game_screen is not None, "Display not initialized."

    window_width, window_height = window_size
    width, height = game_screen_size
    resized_height: int = round(window_height * display_ratio)
    resized_width: int = width * resized_height // height
    resized_height = round(resized_height * display_flat)

    black_color = 255 * fade_black
    game_screen.fill((black_color, black_color, black_color), special_flags=BLEND_RGB_SUB)
    resized_game_screen: Surface = transform.scale(game_screen, (resized_width, resized_height))
    rotated_game_screen: Surface = transform.rotate(resized_game_screen, display_rotate)

    resized_width, resized_height = rotated_game_screen.get_size()

    pos_x: int = (window_width - resized_width) // 2
    pos_y: int = (window_height - resized_height) // 2

    window.blit(rotated_game_screen, (pos_x, pos_y))

    top_layer_scaled: Surface = transform.scale(window_top_layer, window_size)
    window.blit(top_layer_scaled, (0, 0))

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
