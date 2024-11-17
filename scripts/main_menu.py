from enum import Enum

from pygame import Surface

from scripts.input_manager import down_pressed, up_pressed, submit
from scripts import display, textures, game


class SubMenu(Enum):
    """ Enum class for the main menu submenus.
    """
    NONE = 0
    SETTINGS = 1
    CREDITS = 2


class Options(Enum):
    """ Enum class for the main menu options.
    """
    PLAY = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3


current_submenu: SubMenu = SubMenu.NONE
selected_option: Options = Options.PLAY


def run_main_menu():
    """ Display the main menu and let the player choose an option.
    """

    match current_submenu:
        case SubMenu.NONE:
            run_main_menu_none()
        case SubMenu.SETTINGS:
            run_main_menu_settings()
        case SubMenu.CREDITS:
            run_main_menu_credits()
        case _:
            raise ValueError("Invalid submenu")


def run_main_menu_none():
    global selected_option, current_submenu

    if down_pressed():
        selected_option = Options((selected_option.value + 1) % 4)
    elif up_pressed():
        selected_option = Options((selected_option.value - 1) % 4)

    if submit():
        match selected_option:
            case Options.PLAY:
                # todo: animation to enter the game
                game.set_game_state(game.GameState.GAME)
            case Options.SETTINGS:
                current_submenu = SubMenu.SETTINGS
            case Options.CREDITS:
                current_submenu = SubMenu.CREDITS
            case Options.QUIT:
                exit()
            case _:
                raise ValueError("Invalid option")

    display.game_screen.blit(textures.main_menu, (0, 0))

    display.window_top_layer.blit(textures.main_menu_title, (0, 0))

    for i in range(4):
        y = 300 + i * 100
        button: Surface
        button = textures.main_menu_buttons_selected[i] if i == selected_option.value else textures.main_menu_buttons[i]
        display.window_top_layer.blit(button, (0, y))


def run_main_menu_settings():
    global current_submenu
    print("TODO")
    current_submenu = SubMenu.NONE


def run_main_menu_credits():
    global current_submenu
    print("TODO")
    current_submenu = SubMenu.NONE
