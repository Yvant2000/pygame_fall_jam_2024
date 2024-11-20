from random import choice as random_choice, randint
from typing import Self

from pygame import Surface, Rect
from pysidocast import Scene
from scripts import player, textures, display, input_manager


class Room:
    def __init__(self, pos: tuple[int, int]):
        from scripts.game_object import GameObject
        from scripts.objects import Chandelier

        self.pos: tuple[int, int] = pos
        self.scene = Scene()
        self.size: tuple[int, int] = 8, 8
        self.height: float = 4
        self.objects: list[GameObject] = [Chandelier()]  # Door((0, 3.99), True, (pos[0], pos[1] + 1))
        self.pos: tuple[int, int]
        self._loaded: bool = False
        self.collisions: list[Rect] = []

        # keep this method as small as possible, all the heavy load must be in static_loads and dynamic_loads

    def connect_to(self, other: Self):
        """Adds a door between two rooms"""
        assert (self.pos[0] == other.pos[0] or self.pos[1] == other.pos[1]) and (
                abs(self.pos[0] + self.pos[1] - other.pos[0] - other.pos[1]) == 1
        ), "rooms must be adjacent"
        from scripts.objects import Door

        if self.pos[0] == other.pos[0]:
            if self.pos[1] < other.pos[1]:
                self.objects.append(Door((0, self.size[1] // 2 - 0.01), True, other.pos))
                other.objects.append(Door((0, - other.size[1] // 2 + 0.01), True, self.pos))
            else:
                self.objects.append(Door((0, - self.size[1] // 2 + 0.01), True, other.pos))
                other.objects.append(Door((0, other.size[1] // 2 - 0.01), True, self.pos))
        else:
            if self.pos[0] < other.pos[0]:
                self.objects.append(Door((self.size[0] // 2 - 0.01, 0), False, other.pos))
                other.objects.append(Door((- other.size[0] // 2 + 0.01, 0), False, self.pos))
            else:
                self.objects.append(Door((- self.size[0] // 2 + 0.01, 0), False, other.pos))
                other.objects.append(Door((other.size[0] // 2 - 0.01, 0), False, self.pos))

    def static_loads(self):
        wall_index: int = randint(0, textures.wall_count - 1)
        wall_sprite: Surface = textures.merge_wall(textures.walls_bot[wall_index], textures.walls_top[wall_index])
        wall_texture: Surface = random_choice(textures.textures)

        wall_x: Surface = textures.repeat_layered(
            wall_sprite, self.size[0] // 2, 1, wall_texture, self.size[0] // 2 - 1, 3
        )
        wall_z: Surface = textures.repeat_layered(
            wall_sprite, self.size[1] // 2, 1, wall_texture, self.size[1] // 2 - 1, 3
        )

        x = self.size[0]
        y: float = self.height
        z = self.size[1]
        half_x: float = x / 2
        half_z: float = z / 2

        self.scene.add_wall(wall_x, (-half_x, y, half_z), (half_x, 0, half_z))
        self.scene.add_wall(wall_x, (half_x, y, -half_z), (-half_x, 0, -half_z))
        self.scene.add_wall(wall_z, (-half_x, y, -half_z), (-half_x, 0, half_z))
        self.scene.add_wall(wall_z, (half_x, y, half_z), (half_x, 0, -half_z))

        floor_sprite: Surface = random_choice(textures.floors)
        floor_texture = random_choice(textures.textures)
        floor: Surface = textures.repeat_layered(
            floor_sprite, self.size[0] // 2, self.size[1] // 2,
            floor_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        self.scene.add_surface(floor, (-half_x, 0, -half_z), (half_x, 0, -half_z), (-half_x, 0, half_z))

        ceiling_sprite: Surface = random_choice(textures.ceilings)
        ceiling_texture = random_choice(textures.textures)
        ceiling: Surface = textures.repeat_layered(
            ceiling_sprite, self.size[0] // 2, self.size[1] // 2,
            ceiling_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        self.scene.add_surface(ceiling, (-half_x, y, -half_z), (-half_x, y, half_z), (half_x, y, -half_z))

        self.collisions.append(Rect(-x, -half_z, half_x, z))
        self.collisions.append(Rect(-half_x, -z, x, half_z))
        self.collisions.append(Rect(half_x, -half_z, half_x, z))
        self.collisions.append(Rect(-half_x, half_z, x, half_z))

        for game_object in self.objects:
            game_object.static_load(self)

        self._loaded = True

    def dynamic_loads(self):
        for game_object in self.objects:
            game_object.dynamic_load(self)

    def handle_interactions(self):
        player_pointer = player.get_pointer(self.scene)

        # self.scene.add_wall(
        #     textures.chandelier,
        #     (player_pointer[0]-0.4, player_pointer[1]-0.4, player_pointer[2]-0.4),
        #     (player_pointer[0]+0.4, player_pointer[1]+0.4, player_pointer[2]+0.4),
        #     rm=True
        # )  # test ot pointer position

        for game_object in self.objects:
            if game_object.can_interact(player_pointer):
                if input_manager.click():
                    game_object.interact()
                break

    def display(self):
        assert self._loaded, "should have called static_loads and dynamic_loads before calling display"

        self.scene.add_light(player.position, 2.5)  # player light

        render_distance: float = (self.size[0] ** 2 + self.size[1] ** 2) ** 0.5  # gives more depth to the scene

        self.scene.render(
            display.game_screen, player.position, player.angle_x, player.angle_y, player.fov, threads=-1,
            view_distance=render_distance
        )
        self.scene.clear_lights()

    def get_collision(self):
        return self.collisions
