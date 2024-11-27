from random import choice as random_choice
from math import cos, sin, radians

from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import player, textures


def rcos(angle: float) -> float:
    return cos(radians(angle))


def rsin(angle: float) -> float:
    return sin(radians(angle))


class Pillar(GameObject):
    def __init__(self, position: tuple[float, float]):
        super().__init__()
        self.position = (position[0], 0.0, position[1])
        self.image = random_choice(textures.pillars)

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.2, self.position[2] - 0.2, 0.4, 0.4)

    def static_load(self, room: Room):
        pass

    def dynamic_load(self, room: Room):
        scene = room.scene

        w = 0.4
        h = 2.2

        pa = player.angle_y + 90

        scene.add_wall(
            self.image,
            (self.position[0] - w * rcos(pa), self.position[1] + h, self.position[2] - w * rsin(pa)),
            (self.position[0] + w * rcos(pa), self.position[1], self.position[2] + w * rsin(pa)),
            rm=True
        )
