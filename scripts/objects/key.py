from typing import Generator
from math import cos, sin

from scripts.coroutine_manager import create_coroutine
from scripts.game_object import GameObject
from scripts import textures, player, display
from scripts.room import Room


class Key(GameObject):
    def __init__(self, position: tuple[float, float, float]):
        super().__init__()
        self.image = textures.key
        self.buffer = self.image.copy()
        self.is_interactable = True
        self.position = position
        self.time: float = 0
        self.hidden = False

    def static_load(self, room: Room):
        return

    def dynamic_load(self, room: Room):
        if self.hidden:
            return

        self.time += display.delta_time * 2

        mult_x = sin(self.time)
        mult_z = cos(self.time)

        width = 0.28
        height = 0.28

        scene = room.scene
        scene.add_wall(
            self.buffer,
            (self.position[0] - width * mult_x, self.position[1] + height, self.position[2] - width * mult_z),
            (self.position[0] + width * mult_x, self.position[1], self.position[2] + width * mult_z),
            rm=True
        )

    def interact(self):
        player.key_count += 1
        self.is_interactable = False
        create_coroutine(self.pickup())
        # todo sound

    def pickup(self) -> Generator:
        up_velocity = 2.0
        while self.position[1] > 0.0:
            self.position = (
                self.position[0],
                self.position[1] + up_velocity * display.delta_time,
                self.position[2]
            )
            up_velocity -= 5.0 * display.delta_time
            yield

        self.hidden = True
