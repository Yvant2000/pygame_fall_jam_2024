from random import random
from math import cos, sin, pi, radians, atan2

from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import player, textures


def rcos(angle: float) -> float:
    return cos(radians(angle))


def rsin(angle: float) -> float:
    return sin(radians(angle))


class LeatherChair(GameObject):
    def __init__(self, position: tuple[float, float]):
        super().__init__()
        self.position = position[0], 0.0, position[1]
        self.angle = random() * 360

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.5, self.position[2] - 0.5, 1, 1)

    def static_load(self, room):
        pass

    def dynamic_load(self, room: Room):
        scene = room.scene

        w = 0.8
        h = 1.6

        player_pos = player.position
        dx = self.position[0] - player_pos[0]
        dz = self.position[2] - player_pos[2]
        angle = (180 + 180 / pi * -atan2(dz, dx))

        pa = player.angle_y + 90

        # angle = (self.angle - angle) % 360
        image_index = int(angle * len(textures.leather_chair) / 360)
        image = textures.leather_chair[image_index]

        scene.add_wall(
            image,
            (self.position[0] - w * rcos(pa), self.position[1] + h, self.position[2] - w * rsin(pa)),
            (self.position[0] + w * rcos(pa), self.position[1], self.position[2] + w * rsin(pa)),
            rm=True
        )
