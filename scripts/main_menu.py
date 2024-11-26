from enum import Enum
from math import sin
from typing import Generator

from pygame import Surface

from scripts.input_manager import down_pressed, up_pressed, submit
from scripts.easing import ease_out_back, ease_out_bounce, ease_out_expo
from scripts.coroutine_manager import create_coroutine
from scripts import display, textures, game, manor, sounds


class Options(Enum):
    """ Enum class for the main menu options.
    """
    PLAY = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3


selected_option: Options = Options.PLAY

title_y: int = 0
option_x: int = 0
timer: float = 0

settings_open: bool = False
settings_x_pad: int = 1000
settings_selected: int = 2
credits_open: bool = False
credit_y_pad: int = 1000
quit_menu: bool = False
fullscreen: bool = True


def run_main_menu():
    """ Display the main menu and let the player choose an option.
    """

    global selected_option, timer, credits_open, quit_menu, settings_open, settings_selected, fullscreen

    if settings_open:
        credits_open = False
        if down_pressed():
            settings_selected = (settings_selected + 1) % 3
            sounds.menu_down.play()
        elif up_pressed():
            settings_selected = (settings_selected - 1) % 3
            sounds.menu_up.play()
        elif submit():
            sounds.menu_select.play()
            match settings_selected:
                case 0:
                    fullscreen = not fullscreen
                    display.init_display(fullscreen)
                case 1:
                    manor.map_displayed = not manor.map_displayed
                case 2:
                    settings_open = False
    else:
        if down_pressed():
            selected_option = Options((selected_option.value + 1) % 4)
            sounds.menu_down.play()
        elif up_pressed():
            selected_option = Options((selected_option.value - 1) % 4)
            sounds.menu_up.play()
        elif submit():
            match selected_option:
                case Options.PLAY:
                    sounds.menu_start.play()
                    quit_menu = True
                    create_coroutine(start_game_animation())
                case Options.SETTINGS:
                    sounds.menu_select.play()
                    settings_open = True
                case Options.CREDITS:
                    sounds.menu_select.play()
                    credits_open = not credits_open
                case Options.QUIT:
                    exit()
                case _:
                    raise ValueError("Invalid option")

    display.game_screen.blit(textures.main_menu, (0, 0))

    display.window_top_layer.blit(textures.main_menu_title, (0, title_y))

    for i in range(4):
        y = 250 + i * 100
        button: Surface
        button = textures.main_menu_buttons_selected[i] if i == selected_option.value else textures.main_menu_buttons[i]
        display.window_top_layer.blit(button, (option_x, y))

    display.display_rotate = sin(timer) * 1
    timer += display.delta_time * 2

    display_credits()
    display_settings()


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


def display_settings():
    global settings_x_pad

    if settings_open:
        settings_x_pad -= 1500 * display.delta_time
        if settings_x_pad < 0:
            settings_x_pad = 0
    else:
        settings_x_pad += 2000 * display.delta_time
        if settings_x_pad > 1000:
            settings_x_pad = 1000

    pos_x = display.window_top_layer.get_width() - textures.options_buttons[1].get_width() + settings_x_pad + 50
    pos_y = 650
    height = textures.options_buttons[0].get_height()

    if settings_selected == 0:
        display.window_top_layer.blit(textures.options_buttons_selected[0], (pos_x, pos_y))
    else:
        display.window_top_layer.blit(textures.options_buttons[0], (pos_x, pos_y))

    pos_y += height

    if settings_selected == 1:
        if manor.map_displayed:
            display.window_top_layer.blit(textures.options_buttons_selected[1], (pos_x, pos_y))
        else:
            display.window_top_layer.blit(textures.options_buttons_selected[2], (pos_x, pos_y))
    else:
        if manor.map_displayed:
            display.window_top_layer.blit(textures.options_buttons[1], (pos_x, pos_y))
        else:
            display.window_top_layer.blit(textures.options_buttons[2], (pos_x, pos_y))

    pos_y += height

    if settings_selected == 2:
        display.window_top_layer.blit(textures.options_buttons_selected[3], (pos_x, pos_y))
    else:
        display.window_top_layer.blit(textures.options_buttons[3], (pos_x, pos_y))


def intro_animation() -> Generator:
    """ Extends the game screen over time.
    """
    global title_y, option_x

    display.display_flat = 0.0
    display.display_ratio = 0.0
    yield

    progress: float = 0.0

    while progress < 1 and not quit_menu:
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

    display.fade_black = 0.0
    display.display_ratio = 0.0
    # loading = textures.loading
    # display.window_top_layer.blit(
    #     loading,
    #     (display.window_top_layer.get_width() // 2 - loading.get_width() // 2,
    #      display.window_top_layer.get_height() // 2 - loading.get_height() // 2)
    # )
    # TODO: if games takes too long to load, display a loading screen
    yield

    display.display_ratio = 1.0
    display.display_rotate = 0.0
    display.fade_black = 1.0
    game.start_game()
    progress = 1.0

    while progress > 0:
        delta_time = display.get_delta_time() / 2
        display.fade_black = progress
        yield
        progress -= delta_time

    display.fade_black = 0.0
