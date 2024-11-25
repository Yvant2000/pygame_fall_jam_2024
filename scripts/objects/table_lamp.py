from random import random

from pysidocast import Scene

from scripts.game_object import GameObject
from scripts.room import Room, textures


class TableLamp(GameObject):
    def __init__(self):
        super().__init__()
        self.image = textures.table_lamp

        min_color = 0.85
        max_color = 1.05
        delta = max_color - min_color
        self.r = min_color + random() * delta
        self.g = min_color + random() * delta
        self.b = min_color + random() * delta

        average = (self.r + self.g + self.b) / 3
        self.intensity = 1 / average

    def static_load(self, room: Room):
        table_height = 0.85
        lamp_height = 1.0 + table_height
        width = 0.3

        scene = room.scene

        scene.add_wall(self.image, (-width, lamp_height, -width), (width, table_height, width))
        scene.add_wall(self.image, (-width, lamp_height, width), (width, table_height, -width))

    def dynamic_load(self, room: Room):
        scene: Scene = room.scene
        scene.add_light(
            (0, 1.0, 0), intensity=5 * self.intensity,
            red=self.r, green=self.g, blue=self.b
        )  # room light
