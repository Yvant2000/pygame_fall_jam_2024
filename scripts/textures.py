from typing import Final
from os.path import join as join_path

from pygame import Surface, image as pg_image
from pygame.transform import scale, flip
from pygame.constants import BLEND_RGB_MULT

images_folder: str = join_path("assets", "images")


def load_image(path: str, *var_path: str) -> Surface:
    full_path = join_path(images_folder, f"{join_path(path, *var_path)}.png")
    image = pg_image.load(full_path).convert_alpha()
    return image


def merge_wall(bottom_image: Surface, top_image: Surface) -> Surface:
    """ Merge two images into one, placing the first image bellow the second image.
    :param bottom_image: The image that will be placed bellows.
    :param top_image: The image that will be placed on top.
    :return: The merged image.
    """

    width: int = max(bottom_image.get_width(), top_image.get_width())
    height: int = bottom_image.get_height() + top_image.get_height()

    merged_image: Surface = Surface((width, height)).convert_alpha()
    merged_image.blit(top_image, (0, 0))
    merged_image.blit(bottom_image, (0, top_image.get_height()))

    return merged_image


def merge_carpet(carpet_image: Surface) -> Surface:
    """ Merge a carpet image with itself to create a bigger carpet.
    A carpet image is just a corner of the full carpet.
    :param carpet_image:
    :return:
    """

    width, height = carpet_image.get_size()
    merged_image: Surface = Surface((width * 2, height * 2)).convert_alpha()

    merged_image.blit(carpet_image, (0, 0))
    merged_image.blit(flip(carpet_image, True, False), (width, 0))
    merged_image.blit(flip(carpet_image, False, True), (0, height))
    merged_image.blit(flip(carpet_image, True, True), (width, height))

    return merged_image


def repeat(image: Surface, x: int, y: int) -> Surface:
    """ Repeat an image multiple times in the x and y-axis.
    :param image: The image to repeat.
    :param x: The number of repetitions in the x-axis.
    :param y: The number of repetitions in the y-axis.
    """
    assert x > 0 and y > 0, "The number of repetitions must be greater than 0."

    width, height = image.get_size()
    repeated_image: Surface = Surface((width * x, height * y)).convert_alpha()

    for i in range(x):
        for j in range(y):
            repeated_image.blit(image, (i * width, j * height))

    return repeated_image


def repeat_layered(image: Surface, x: int, y: int, layer: Surface, l_x: int, l_y: int) -> Surface:
    """ Repeat an image multiple times in the x and y-axis. \n
    The image is then covered by a semi-transparent layer to limit the impression of repetition.
    :param image: The image to repeat.
    :param x: The number of repetitions in the x-axis.
    :param y: The number of repetitions in the y-axis.
    :param layer: The layer to cover the repeated image
    :param l_y:
    :param l_x:
    """

    repeated_image: Surface = repeat(image, x, y)
    repeat_layer: Surface = repeat(layer, l_x, l_y)
    scaled_layer: Surface = scale(repeat_layer, repeated_image.get_size())
    repeated_image.blit(scaled_layer, (0, 0), special_flags=BLEND_RGB_MULT)

    return repeated_image


# Menus
main_menu: Surface = load_image("menu", "main")
main_menu_title: Surface = load_image("menu", "title")
menu_credits: Surface = load_image("menu", "credits")
end_screen: Surface = load_image("menu", "end")
end_message: Surface = load_image("menu", "end_message")
loading: Surface = load_image("menu", "loading")

mm_buttons: tuple[str, ...] = ("play", "settings", "credits", "quit")
main_menu_buttons: tuple[Surface, ...] = tuple(load_image("menu", "buttons", button) for button in mm_buttons)
main_menu_buttons_selected: tuple[Surface, ...] = tuple(
    load_image("menu", "buttons", f"{button}_selected") for button in mm_buttons
)
del mm_buttons

opt_buttons: tuple[str, ...] = ("fullscreen", "display_map_on", "display_map_off", "back")
options_buttons: tuple[Surface, ...] = tuple(load_image("menu", "buttons", button) for button in opt_buttons)
options_buttons_selected: tuple[Surface, ...] = tuple(
    load_image("menu", "buttons", f"{button}_selected") for button in opt_buttons
)
del opt_buttons

# Rooms
walls_bot: tuple[Surface, ...] = tuple(load_image("rooms", "walls", f"wall{i}_bot") for i in range(2))
walls_top: tuple[Surface, ...] = tuple(load_image("rooms", "walls", f"wall{i}_top") for i in range(2))
wall_count: Final[int] = len(walls_bot)
assert wall_count == len(walls_top)

ceilings: tuple[Surface, ...] = tuple(load_image("rooms", "ceilings", f"ceiling{i}") for i in range(4))
floors: tuple[Surface, ...] = tuple(load_image("rooms", "floors", f"floor{i}") for i in range(4))

textures: tuple[Surface, ...] = tuple(load_image("rooms", "textures", f"texture{i}") for i in range(4))

carpets: tuple[Surface, ...] = tuple(load_image("rooms", "carpets", f"carpet{i}") for i in range(4))

# Props
doors: tuple[Surface, ...] = tuple(load_image("props", "doors", f"door{i}") for i in range(4))
chandelier: Surface = load_image("props", "lights", f"chandelier")
ending_door: Surface = load_image("props", "doors", "ending_door")
table_tops: tuple[Surface, ...] = tuple(load_image("props", "tables", f"top{i}") for i in range(4))
table_side: Surface = load_image("props", "tables", "side")
table_lamp: Surface = load_image("props", "lights", "table_lamp")
key: Surface = load_image("props", "key")
small_table_front: Surface = load_image("props", "tables", "small_front")
small_table_side: Surface = load_image("props", "tables", "small_side")
