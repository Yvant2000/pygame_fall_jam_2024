from random import random
from math import pi, cos, sin

from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import textures


class WoodenChair(GameObject):
    def __init__(self, position: tuple[float, float], angle: float | None = None, height: float = 0):
        super().__init__()
        self.position = (position[0], 0.0, position[1])
        self.angle = angle if angle is not None else random() * 2 * pi
        self.height = height

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.3, self.position[2] - 0.3, 0.6, 0.6)

    def static_load(self, room: Room):
        scene = room.scene

        seat = textures.wooden_chair_seat
        front = textures.wooden_chair_front
        back = textures.wooden_chair_back

        seat_height = 0.65
        back_height = 1.5

        w = 0.5
        angle = self.angle
        cos_w = cos(angle) * w
        sin_w = sin(angle) * w

        scene.add_quad(
            seat,
            (self.position[0] - cos_w, seat_height+self.height, self.position[2] - sin_w),
            (self.position[0] + sin_w, seat_height+self.height, self.position[2] - cos_w),
            (self.position[0] + cos_w, seat_height+self.height, self.position[2] + sin_w),
            (self.position[0] - sin_w, seat_height+self.height, self.position[2] + cos_w)
        )

        scene.add_wall(
            back,
            (self.position[0] - cos_w, back_height+self.height, self.position[2] - sin_w),
            (self.position[0] + sin_w, self.height, self.position[2] - cos_w)
        )

        w = 0.45
        cos_w = cos(angle) * w
        sin_w = sin(angle) * w

        scene.add_wall(
            front,
            (self.position[0] + cos_w, seat_height+self.height, self.position[2] + sin_w),
            (self.position[0] - sin_w, self.height, self.position[2] + cos_w)
        )
