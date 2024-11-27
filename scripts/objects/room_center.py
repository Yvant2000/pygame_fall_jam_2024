from random import choice as random_choice, randint

from pygame.surface import Surface
from pygame.rect import FRect

from scripts.game_object import GameObject
from scripts.room import Room
from scripts import textures


class RoomCenter(GameObject):
    def __init__(self, texture_x: Surface, texture_z: Surface):  # U R D L
        super().__init__()
        self.textures_x = texture_x
        self.textures_z = texture_z

    @property
    def colliders(self):
        yield FRect(-1, -1, 2, 2)

    def static_load(self, room: Room):
        scene = room.scene
        x = room.size[0] / 8
        y = room.height
        z = room.size[1] / 8

        texture_x2 = self.textures_x.copy()
        texture_z2 = self.textures_z.copy()

        if randint(0, 3) == 0:
            self.textures_x.blit(
                random_choice(textures.clocks),
                (self.textures_x.get_width() // 2 - 32, self.textures_x.get_height() // 2 - 32)
            )

        if randint(0, 3) == 0:
            self.textures_z.blit(
                random_choice(textures.clocks),
                (self.textures_z.get_width() // 2 - 32, self.textures_z.get_height() // 2 - 32)
            )

        if randint(0, 3) == 0:
            texture_x2.blit(
                random_choice(textures.clocks), (texture_x2.get_width() // 2 - 32, texture_x2.get_height() // 2 - 32)
            )

        if randint(0, 3) == 0:
            texture_z2.blit(
                random_choice(textures.clocks), (texture_z2.get_width() // 2 - 32, texture_z2.get_height() // 2 - 32)
            )

        scene.add_wall(self.textures_x, (-x, y, -z), (x, 0.0, -z))
        scene.add_wall(self.textures_z, (-x, y, -z), (-x, 0.0, z))
        scene.add_wall(texture_x2, (-x, y, z), (x, 0.0, z))
        scene.add_wall(texture_z2, (x, y, -z), (x, 0.0, z))
