from random import random

from pysidocast import Scene

from scripts.room import Room
from scripts.game_object import GameObject
from scripts.textures import chandelier


class Chandelier(GameObject):
    def __init__(self):
        super().__init__()
        self.image = chandelier

        min_color = 0.7
        max_color = 1.1
        delta = max_color - min_color
        self.r = min_color + random() * delta
        self.g = min_color + random() * delta
        self.b = min_color + random() * delta

        average = (self.r + self.g + self.b) / 3
        self.intensity = 1 / average

    def static_load(self, room: Room):
        scene: Scene = room.scene
        scene.add_wall(self.image, (-0.8, room.height, 0), (0.8, room.height - 1.6, 0))
        scene.add_wall(self.image, (0, room.height, -0.8), (0, room.height - 1.6, 0.8))

    def dynamic_load(self, room: Room):
        scene: Scene = room.scene
        scene.add_light(
            (0, room.height, 0), intensity=4 * self.intensity, direction=(0, 0, 0),
            red=self.r, green=self.g, blue=self.b
        )  # room light
        scene.add_light(
            (0, room.height - 0.8, 0), intensity=2 * self.intensity, red=self.r, green=self.g, blue=self.b
        )  # ceiling light
