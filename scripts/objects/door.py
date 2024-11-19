from random import choice as random_choice
from typing import Generator

from pygame import Vector3, Surface
from pysidocast import Scene

from scripts.coroutine_manager import create_coroutine
from scripts.display import get_delta_time
from scripts.game_object import GameObject
from scripts.textures import doors
from scripts import input_manager, display, player


class Door(GameObject):
    def __init__(self, position: tuple[float, float], axis_x: bool, destination: tuple[int, int]):
        super().__init__((position[0], 1.15, position[1]))
        self.axis_x: bool = axis_x
        self.image: Surface = random_choice(doors)
        self.buffer: Surface = self.image.copy()
        self._is_lighted: bool = False
        self.destination: tuple[int, int] = destination
        self.is_interactable = True

    def static_load(self, room):
        rayon = 1.0
        height = 2.3
        half_height = height / 2

        scene: Scene = room.scene
        if self.axis_x:
            scene.add_wall(
                self.buffer,
                (self.position[0] - rayon, self.position[1] + half_height, self.position[2]),
                (self.position[0] + rayon, self.position[1] - half_height, self.position[2])
            )
        else:
            scene.add_wall(
                self.buffer,
                (self.position[0], self.position[1] + half_height, self.position[2] - rayon),
                (self.position[0], self.position[1] - half_height, self.position[2] + rayon)
            )

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
