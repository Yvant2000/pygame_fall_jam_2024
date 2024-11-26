from random import choice as random_choice, random
from math import pi, cos, sin

from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import textures


class SmallTable(GameObject):
    def __init__(self, position: tuple[float, float]):
        super().__init__()
        self.position = (position[0], 0.75, position[1])

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.5, self.position[2] - 0.5, 1.0, 1.0)

    def static_load(self, room: Room):
        scene = room.scene

        top = random_choice(textures.table_tops)
        side = textures.small_table_side
        front = textures.small_table_front

        w = 0.5
        angle = random() * 2 * pi

        cos_w = cos(angle) * w
        sin_w = sin(angle) * w

        scene.add_quad(
            top,
            (self.position[0] - cos_w, self.position[1], self.position[2] - sin_w),
            (self.position[0] + sin_w, self.position[1], self.position[2] - cos_w),
            (self.position[0] + cos_w, self.position[1], self.position[2] + sin_w),
            (self.position[0] - sin_w, self.position[1], self.position[2] + cos_w)
        )

        scene.add_wall(
            front,
            (self.position[0] - cos_w, self.position[1], self.position[2] - sin_w),
            (self.position[0] + sin_w, 0.0, self.position[2] - cos_w)
        )

        scene.add_wall(
            side,
            (self.position[0] + sin_w, self.position[1], self.position[2] - cos_w),
            (self.position[0] + cos_w, 0.0, self.position[2] + sin_w)
        )

        scene.add_wall(
            side,
            (self.position[0] + cos_w, self.position[1], self.position[2] + sin_w),
            (self.position[0] - sin_w, 0.0, self.position[2] + cos_w)
        )

        scene.add_wall(
            side,
            (self.position[0] - sin_w, self.position[1], self.position[2] + cos_w),
            (self.position[0] - cos_w, 0.0, self.position[2] - sin_w)
        )
