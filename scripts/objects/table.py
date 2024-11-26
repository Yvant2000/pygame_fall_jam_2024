from random import choice as random_choice, randint

from pygame.rect import FRect
from pygame.transform import rotate, scale2x

from scripts import textures
from scripts.game_object import GameObject
from scripts.room import Room


class Table(GameObject):

    def __init__(self):
        super().__init__()
        self.top = random_choice(textures.table_tops).copy()

        if randint(0, 1) == 0:
            self.top = scale2x(scale2x(self.top))
            paper = textures.paper.copy()
            paper_rot = rotate(paper, randint(0, 360))
            self.top.blit(
                paper_rot,
                (randint(0, self.top.get_width() - paper_rot.get_width()),
                 (randint(0, self.top.get_height() - paper_rot.get_height())))
            )

        self.side = textures.table_side

    @property
    def colliders(self) -> list[FRect]:
        yield FRect(-1, -1, 2, 2)

    def static_load(self, room: Room):
        height: float = 0.85
        w = 0.8
        fw = 1

        scene = room.scene
        scene.add_wall(self.side, (-w, height, -fw), (-w, 0, fw))
        scene.add_wall(self.side, (-fw, height, w), (fw, 0, w))
        scene.add_wall(self.side, (w, height, fw), (w, 0, -fw))
        scene.add_wall(self.side, (fw, height, -w), (-fw, 0, -w))

        scene.add_surface(self.top, (-fw, height, -fw), (-fw, height, fw), (fw, height, -fw))
