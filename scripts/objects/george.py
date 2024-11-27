from math import cos, sin, radians

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import player, textures


def rcos(angle: float) -> float:
    return cos(radians(angle))


def rsin(angle: float) -> float:
    return sin(radians(angle))


class George(GameObject):
    def __init__(self, position: tuple[float, float, float]):
        super().__init__()
        self.position = position

    def static_load(self, room):
        pass

    def dynamic_load(self, room: Room):
        scene = room.scene

        w = 0.3
        h = 0.7

        distance = (self.position[0] - player.position[0]) ** 2 + (self.position[2] - player.position[2]) ** 2

        pa = player.angle_y + 90

        image = textures.george

        scene.add_wall(
            image,
            (self.position[0] - w * rcos(pa), self.position[1] + h, self.position[2] - w * rsin(pa)),
            (self.position[0] + w * rcos(pa), self.position[1], self.position[2] + w * rsin(pa)),
            rm=True,
            alpha=min(1.0, max(0.0, 1.0 - distance / 6.0 + 0.4))
        )
