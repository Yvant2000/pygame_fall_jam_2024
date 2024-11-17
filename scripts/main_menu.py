from enum import Enum
from math import sin
from typing import Generator

from pygame import Surface

from scripts.input_manager import down_pressed, up_pressed, submit
from scripts import display, textures, game
from scripts.easing import ease_out_back, ease_out_bounce, ease_out_expo
from scripts.coroutine_manager import create_coroutine


class SubMenu(Enum):
    """ Enum class for the main menu submenus.
    """
    NONE = 0
    SETTINGS = 1


class Options(Enum):
    """ Enum class for the main menu options.
    """
    PLAY = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3


current_submenu: SubMenu = SubMenu.NONE
selected_option: Options = Options.PLAY

title_y: int = 0
option_x: int = 0
timer: float = 0

credits_open: bool = False
credit_y_pad: int = 1000


def run_main_menu():
    """ Display the main menu and let the player choose an option.
    """

    match current_submenu:
        case SubMenu.NONE:
            run_main_menu_none()
        case SubMenu.SETTINGS:
            run_main_menu_settings()
        case _:
            raise ValueError("Invalid submenu")


def run_main_menu_none():
    global selected_option, current_submenu, timer, credits_open

    if down_pressed():
        selected_option = Options((selected_option.value + 1) % 4)
    elif up_pressed():
        selected_option = Options((selected_option.value - 1) % 4)

    if submit():
        match selected_option:
            case Options.PLAY:
                create_coroutine(start_game_animation())
            case Options.SETTINGS:
                current_submenu = SubMenu.SETTINGS
            case Options.CREDITS:
                credits_open = not credits_open
            case Options.QUIT:
                exit()
            case _:
                raise ValueError("Invalid option")

    display.game_screen.blit(textures.main_menu, (0, 0))

    display.window_top_layer.blit(textures.main_menu_title, (0, title_y))

    for i in range(4):
        y = 300 + i * 100
        button: Surface
        button = textures.main_menu_buttons_selected[i] if i == selected_option.value else textures.main_menu_buttons[i]
        display.window_top_layer.blit(button, (option_x, y))

    display.display_rotate = sin(timer) * 1
    timer += display.delta_time * 2

    display_credits()


def display_credits():
    global credit_y_pad

    credit_image: Surface = textures.menu_credits
    credits_height: int = credit_image.get_height()

    if credits_open:
        credit_y_pad -= 1000 * display.delta_time
        if credit_y_pad < 0:
            credit_y_pad = 0
    else:
        credit_y_pad += 1500 * display.delta_time
        if credit_y_pad > credits_height:
            credit_y_pad = credits_height

    top_layer: Surface = display.window_top_layer
    credit_x: int = top_layer.get_width() - credit_image.get_width()
    credit_y: int = top_layer.get_height() - credits_height
    display.window_top_layer.blit(textures.menu_credits, (credit_x, credit_y + credit_y_pad))


def run_main_menu_settings():
    global current_submenu
    print("TODO")
    current_submenu = SubMenu.NONE


def run_main_menu_credits():
    global current_submenu
    print("TODO")
    current_submenu = SubMenu.NONE


def intro_animation() -> Generator:
    """ Extends the game screen over time.
    """
    global title_y, option_x

    display.display_flat = 0.0
    display.display_ratio = 0.0
    yield

    progress: float = 0.0

    while progress < 1:
        delta_time = display.get_delta_time()
        progress += delta_time / 3
        display.display_flat = ease_out_back(progress)
        display.display_ratio = ease_out_back(progress) * 0.8
        title_y = -300 * (1 - ease_out_bounce(progress))
        option_x = -750 * (1 - ease_out_expo(progress))
        yield

    display.display_flat = 1.0
    display.display_ratio = 0.8
    title_y = 0
    option_x = 0


def start_game_animation() -> Generator:
    global title_y, option_x
    progress: float = 0.0

    yield

    while progress < 1:
        delta_time = display.get_delta_time()
        display.fade_black = progress
        display.display_ratio = 0.8 + 0.2 * ease_out_back(progress)
        option_x = -750 * ease_out_expo(progress)
        title_y = -300 * ease_out_bounce(progress)
        yield
        progress += delta_time / 2

    display.fade_black = 1.0
    display.display_rotate = 0.0
    game.set_game_state(game.GameState.GAME)
    progress = 1.0
    yield

    while progress > 0:
        delta_time = display.get_delta_time()
        display.fade_black = progress
        yield
        progress -= delta_time

    display.fade_black = 0.0
