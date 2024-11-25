from random import choice as random_choice
from typing import Generator

from pygame import Surface
from pygame.draw import line as draw_line
from pysidocast import Scene

from scripts.coroutine_manager import create_coroutine
from scripts.display import get_delta_time
from scripts.game_object import GameObject
from scripts.textures import doors, lock
from scripts import input_manager, display, player, manor
from scripts.room import Room


class Door(GameObject):
    def __init__(self, position: tuple[float, float], axis_x: bool, positive: bool, destination: tuple[int, int]):
        super().__init__((position[0], 1.15, position[1]))
        self.axis_x: bool = axis_x
        self.positive: bool = positive
        self.image: Surface = random_choice(doors)
        self.buffer: Surface = self.image.copy()
        self._is_lighted: bool = False
        self.destination: tuple[int, int] = destination
        self.is_interactable = True
        self.locked = False

    def static_load(self, room):
        rayon = 1.0
        height = 2.3
        half_height = height / 2

        scene: Scene = room.scene
        if self.axis_x:
            scene.add_wall(
                self.buffer,
                (self.position[0] - rayon, self.position[1] + half_height, self.position[2]),
                (self.position[0] + rayon, self.position[1] - half_height, self.position[2])
            )
        else:
            scene.add_wall(
                self.buffer,
                (self.position[0], self.position[1] + half_height, self.position[2] - rayon),
                (self.position[0], self.position[1] - half_height, self.position[2] + rayon)
            )

    def dynamic_load(self, room: Room):
        if not self.locked:
            return

        rayon = 0.3
        height = 0.7
        half_height = height / 2

        distance_to_player = (player.position[0] - self.position[0]) ** 2 + (player.position[2] - self.position[2]) ** 2
        alpha = max(0.0, min(1.0, 1.0 - distance_to_player / 8.0 + 0.2))

        scene: Scene = room.scene
        if self.axis_x:
            scene.add_wall(
                lock,
                (self.position[0] * 0.98 - rayon, self.position[1] + half_height, self.position[2] * 0.98),
                (self.position[0] * 0.98 + rayon, self.position[1] - half_height, self.position[2] * 0.98),
                rm=True,
                alpha=alpha
            )
        else:
            scene.add_wall(
                lock,
                (self.position[0] * 0.98, self.position[1] + half_height, self.position[2] * 0.98 - rayon),
                (self.position[0] * 0.98, self.position[1] - half_height, self.position[2] * 0.98 + rayon),
                rm=True,
                alpha=alpha
            )

    def interact(self):
        if self.locked:
            if player.key_count > 0:
                player.key_count -= 1
                self.locked = False
                # todo sound
            else:
                # todo sound
                draw_line(
                    manor.manor_map, (150, 50, 50),
                    (player.grid_position[1] * 4 + 1, player.grid_position[0] * 4 + 1),
                    (self.destination[1] * 4 + 1, self.destination[0] * 4 + 1),
                )
                return

        create_coroutine(self.move_to_next_room())

    def move_to_next_room(self) -> Generator:
        input_manager.lock = True
        yield

        progress = 0
        while progress < 1:
            progress += get_delta_time()
            display.fade_black = progress
            yield

        draw_line(
            manor.manor_map, (100, 100, 100),
            (player.grid_position[1] * 4 + 1, player.grid_position[0] * 4 + 1),
            (self.destination[1] * 4 + 1, self.destination[0] * 4 + 1),
        )

        player.grid_position = self.destination
        destination: Room = manor.rooms[self.destination[0]][self.destination[1]]
        size = destination.size
        player.angle_x = 0
        if self.axis_x:
            player.position.x = 0
            if self.positive:
                player.position.z = -size[1] / 2 + 0.5
                player.angle_y = 90
            else:
                player.position.z = size[1] / 2 - 0.5
                player.angle_y = -90
        else:
            player.position.z = 0
            if self.positive:
                player.position.x = -size[0] / 2 + 0.5
                player.angle_y = 0
            else:
                player.position.x = size[0] / 2 - 0.5
                player.angle_y = 180

        input_manager.lock = False

        progress = 0
        while progress < 1:
            progress += get_delta_time() * 2
            display.fade_black = 1 - progress
            yield

        display.fade_black = 0
