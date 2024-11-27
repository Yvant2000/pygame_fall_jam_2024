from math import cos, sin, radians
from random import choice as random_choice

from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import player, textures


def rsin(angle: float) -> float:
    return sin(radians(angle))


def rcos(angle: float) -> float:
    return cos(radians(angle))


class Plant(GameObject):
    def __init__(self, position: tuple[float, float]):
        super().__init__()
        self.position = (position[0], 0.0, position[1])
        self.image = random_choice(textures.plants)

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.3, self.position[2] - 0.3, 0.6, 0.6)

    def static_load(self, room: Room):
        pass

    def dynamic_load(self, room: Room):
        scene = room.scene

        pa = player.angle_y + 90

        w = 0.55
        h = 1.7

        scene.add_wall(
            self.image,
            (self.position[0] - w * rcos(pa), self.position[1] + h, self.position[2] - w * rsin(pa)),
            (self.position[0] + w * rcos(pa), self.position[1], self.position[2] + w * rsin(pa)),
            rm=True
        )
