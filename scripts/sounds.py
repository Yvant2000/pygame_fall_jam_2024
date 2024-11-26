from os.path import join as join_path

from pygame.mixer import Sound, init as mixer_init

mixer_init()

sound_folder: str = join_path("assets", "sounds")


def load_sound(path: str, *var_path: str) -> Sound:
    full_path = join_path(sound_folder, f"{join_path(path, *var_path)}.mp3")
    sound = Sound(full_path)
    return sound


steps: tuple[Sound, ...] = tuple(load_sound("steps", f"step{i}") for i in range(6))
key_pickup: tuple[Sound, ...] = tuple(load_sound("key_pickup", f"key{i}") for i in range(6))
door_closed: tuple[Sound, ...] = tuple(load_sound("door_closed", f"door{i}") for i in range(4))
door_unlocked: tuple[Sound, ...] = tuple(load_sound("door_unlocked", f"door{i}") for i in range(4))
door_opened: tuple[Sound, ...] = tuple(load_sound("door_opened", f"door{i}") for i in range(5))

menu_up: Sound = load_sound("menu", "up")
menu_down: Sound = load_sound("menu", "down")
menu_select: Sound = load_sound("menu", "select")
menu_start: Sound = load_sound("menu", "start")
