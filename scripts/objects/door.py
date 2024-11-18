from random import choice as random_choice
from typing import Generator

from pygame import Vector3, Surface
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_SUB
from pysidocast import Scene

from scripts.coroutine_manager import create_coroutine
from scripts.display import get_delta_time
from scripts.game_object import GameObject
from scripts.textures import doors
from scripts import input_manager, display, player


class Door(GameObject):
    def __init__(self, position: tuple[float, float, float], axis_x: bool, destination: tuple[int, int]):
        self.position: tuple[float, float, float] = position
        self.axis_x: bool = axis_x
        self.image: Surface = random_choice(doors)
        self.buffer: Surface = self.image.copy()
        self.is_lighted: bool = False
        self.destination: tuple[int, int] = destination

    def static_load(self, room):
        rayon = 1.0
        height = 2.3

        scene: Scene = room.scene
        if self.axis_x:
            scene.add_wall(
                self.buffer,
                (self.position[0] - rayon, self.position[1] + height, self.position[2]),
                (self.position[0] + rayon, self.position[1], self.position[2])
            )
        else:
            scene.add_wall(
                self.buffer,
                (self.position[0], self.position[1] + height, self.position[2] - rayon),
                (self.position[0], self.position[1], self.position[2] + rayon)
            )

    def can_interact(self, player_pointer):
        middle: Vector3 = Vector3(self.position)
        middle.y += 1.15

        if Vector3(player_pointer).distance_to(middle) < 0.8:
            if not self.is_lighted:
                self.buffer.fill((50, 50, 50), special_flags=BLEND_RGB_ADD)
                self.is_lighted = True
            return True
        else:
            if self.is_lighted:
                self.buffer.fill((50, 50, 50), special_flags=BLEND_RGB_SUB)
                self.is_lighted = False
            return False

    def interact(self):
        create_coroutine(self.move_to_next_room())

    def move_to_next_room(self) -> Generator:
        input_manager.lock = True
        yield

        progress = 0
        while progress < 1:
            progress += get_delta_time()
            display.fade_black = progress
            yield

        player.grid_position = self.destination
        player.position = Vector3()  # todo
        input_manager.lock = False

        progress = 0
        while progress < 1:
            progress += get_delta_time() * 2
            display.fade_black = 1 - progress
            yield

        display.fade_black = 0
