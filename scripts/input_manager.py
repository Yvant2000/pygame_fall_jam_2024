from pygame import mouse, key, event as pg_event
from pygame.key import ScancodeWrapper
from pygame.constants import K_RETURN, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d, K_z, K_q, K_LCTRL, \
    K_RCTRL, K_LSHIFT, K_RSHIFT

from scripts import display

keys_down: ScancodeWrapper  # keys that are currently down
keys_pressed: set = set()  # keys that were pressed this frame

mouse_rel: tuple[int, int] = 0, 0

lock: bool = False


def refresh_input():
    global keys_down, mouse_rel
    keys_down = key.get_pressed()
    keys_pressed.clear()

    if key.get_focused():  # Place the mouse in the center of the screen when the window is active
        mouse.set_visible(False)  # Hide the mouse
        pg_event.set_grab(True)  # Grab the mouse
        mouse_rel = mouse.get_rel()  # Get the mouse movement since the last frame
        if mouse_rel != (0, 0):
            mouse.set_pos(display.window_size[0] // 2, display.window_size[1] // 2)
    else:
        # Give back the mouse control when the window is not active
        mouse.set_visible(True)
        pg_event.set_grab(False)
        mouse_rel = 0, 0


def set_key_pressed(key_code: int):
    keys_pressed.add(key_code)


def submit() -> bool:
    """ Checks if the player pressed the "submit" key.
    :return: True if the "submit" key is pressed.
    """
    return not lock and any(code in keys_pressed for code in (K_RETURN, K_SPACE))


def up_pressed() -> bool:
    """ Checks if the player pressed the up key.
    :return: True if the up key was pressed this frame.
    """
    return not lock and any(code in keys_pressed for code in (K_UP, K_w, K_z))


def down_pressed() -> bool:
    """ Checks if the player pressed the down key.
    :return: True if the down key was pressed this frame.
    """
    return not lock and any(code in keys_pressed for code in (K_DOWN, K_s))


def horizontal_value() -> float:
    """ Get the horizontal movement value.
    :return: The horizontal movement value.
    """
    if lock:
        return 0

    if any(keys_down[code] for code in (K_LEFT, K_a, K_q)):
        return 1
    if any(keys_down[code] for code in (K_RIGHT, K_d)):
        return -1
    return 0


def vertical_value() -> float:
    """ Get the vertical movement value.
    :return: The vertical movement value.
    """
    if lock:
        return 0

    if any(keys_down[code] for code in (K_UP, K_w, K_z)):
        return 1
    if any(keys_down[code] for code in (K_DOWN, K_s)):
        return -1

    return 0


def get_relative_mouse_movement() -> tuple[int, int]:
    """ Get the relative mouse movement.
    :return: The relative mouse movement.
    """
    if lock:
        return 0, 0

    return mouse_rel


def crouch() -> bool:
    """ Checks if the player pressed the crouch key.
    :return: True if the crouch key was pressed this frame.
    """
    return not lock and any(keys_down[code] for code in (K_LCTRL, K_RCTRL, K_LSHIFT, K_RSHIFT))


def jump() -> bool:
    """ Checks if the player pressed the jump key.
    :return: True if the jump key was pressed this frame.
    """
    return not lock and K_SPACE in keys_pressed


def click() -> bool:
    """ Checks if the player clicked the mouse.
    :return: True if the mouse was clicked this frame.
    """
    return not lock and mouse.get_pressed()[0] or mouse.get_pressed()[2] or K_RETURN in keys_pressed
