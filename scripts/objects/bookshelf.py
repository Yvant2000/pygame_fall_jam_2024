from random import choice as random_choice

from pygame.surface import Surface

from scripts.game_object import GameObject
from scripts import textures
from scripts.room import Room


class Bookshelf(GameObject):
    def __init__(self, distance: float, orientation: bool):
        super().__init__()
        self.distance = distance
        self.orientation = orientation

    def static_load(self, room: Room):
        width, height = textures.bookshelves[0].get_size()
        x = room.size[0] // 2
        y = 2
        repeated: Surface = Surface((width * x, height * y)).convert_alpha()

        for i in range(x):
            for j in range(y):
                repeated.blit(random_choice(textures.bookshelves), (i * width, j * height))

        # repeated: Surface = textures.repeat(image, room.size[0] // 2, 1)
        height = room.height

        if self.orientation:
            room.scene.add_wall(
                repeated, (-room.size[0] / 2, height, self.distance), (room.size[0] / 2, 0.0, self.distance)
            )
        else:
            room.scene.add_wall(
                repeated, (self.distance, height, -room.size[1] / 2), (self.distance, 0.0, room.size[1] / 2)
            )
