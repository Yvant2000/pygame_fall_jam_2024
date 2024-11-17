import pygame
from scripts.display import init_display, update_display, clear_game_screen, get_delta_time

pygame.init()
init_display()

from scripts.game import run_game
from scripts.input_manager import refresh_input, set_key_pressed
from scripts.particles import update_particles
from scripts.coroutine_manager import update_coroutines


def pg_events() -> bool:
    """ Handle pygame events.
    :return: True until the user closes the window.
    """

    refresh_input()

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                set_key_pressed(event.key)

    return True


def main():
    """ Main loop
    """

    while pg_events():
        delta_time: float = get_delta_time()
        clear_game_screen()
        update_particles(delta_time)
        update_coroutines(delta_time)
        run_game()
        update_display()


if __name__ == "__main__":
    main()
