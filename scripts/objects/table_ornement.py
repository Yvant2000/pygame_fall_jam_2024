from random import choice as random_choice
from math import cos, sin, radians

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import textures, player


def rcos(angle: float) -> float:
    return cos(radians(angle))


def rsin(angle: float) -> float:
    return sin(radians(angle))


class TableOrnement(GameObject):
    def __init__(self, position: tuple[float, float, float]):
        super().__init__()
        self.position = position
        self.image = random_choice(textures.ornements)

    def static_load(self, room: Room):
        pass

    def dynamic_load(self, room: Room):
        scene = room.scene

        w = 0.4
        h = 0.7

        pa = player.angle_y + 90

        image = self.image

        scene.add_wall(
            image,
            (self.position[0] - w * rcos(pa), self.position[1] + h, self.position[2] - w * rsin(pa)),
            (self.position[0] + w * rcos(pa), self.position[1], self.position[2] + w * rsin(pa)),
            rm=True
        )
