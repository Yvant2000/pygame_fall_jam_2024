from pygame.rect import FRect
from pygame.surface import Surface

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import textures


class Clock(GameObject):
    def __init__(self, position: tuple[float, float], angle: int):
        super().__init__()
        self.position: tuple[float, float, float] = (position[0], 0.0, position[1])
        self.angle: int = angle

    @property
    def colliders(self):
        yield FRect(self.position[0] - 0.25, self.position[2] - 0.25, 0.5, 0.5)

    def static_load(self, room: Room):
        scene = room.scene

        front: Surface = textures.grandpa_clock_front
        side: Surface = textures.grandpa_clock_side

        pos = self.position
        fw = 0.35
        w = 0.22
        h = 2.2
        l = 0.28

        match self.angle:
            case 0:
                scene.add_wall(front, (pos[0] - fw, h, pos[2] - l), (pos[0] + fw, 0, pos[2] - l))
                scene.add_wall(side, (pos[0] - w, h, pos[2]), (pos[0] - w, 0, pos[2] - l))
                scene.add_wall(side, (pos[0] + w, h, pos[2]), (pos[0] + w, 0, pos[2] - l))
            case 1:
                scene.add_wall(front, (pos[0] + l, h, pos[2] - fw), (pos[0] + l, 0, pos[2] + fw))
                scene.add_wall(side, (pos[0], h, pos[2] - w), (pos[0] + l, 0, pos[2] - w))
                scene.add_wall(side, (pos[0], h, pos[2] + w), (pos[0] + l, 0, pos[2] + w))
            case 2:
                scene.add_wall(front, (pos[0] - fw, h, pos[2] + l), (pos[0] + fw, 0, pos[2] + l))
                scene.add_wall(side, (pos[0] - w, h, pos[2]), (pos[0] - w, 0, pos[2] + l))
                scene.add_wall(side, (pos[0] + w, h, pos[2]), (pos[0] + w, 0, pos[2] + l))
            case 3:
                scene.add_wall(front, (pos[0] - l, h, pos[2] - fw), (pos[0] - l, 0, pos[2] + fw))
                scene.add_wall(side, (pos[0], h, pos[2] - w), (pos[0] - l, 0, pos[2] - w))
                scene.add_wall(side, (pos[0], h, pos[2] + w), (pos[0] - l, 0, pos[2] + w))