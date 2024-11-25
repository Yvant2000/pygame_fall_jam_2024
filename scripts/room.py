from random import choice as random_choice, randint, random
from math import pi, cos, sin
from typing import Self

from pygame import Surface
from pygame import FRect
from pysidocast import Scene
from scripts import player, textures, display, input_manager


class Room:
    def __init__(self, pos: tuple[int, int]):
        from scripts.game_object import GameObject
        from scripts.objects import Chandelier, Table, TableLamp, Door

        self.pos: tuple[int, int] = pos
        self.scene = Scene()
        self.size: tuple[int, int] = 8, 8
        self.height: float = 4
        self.objects: list[GameObject] = []
        self.pos: tuple[int, int]
        self._loaded: bool = False
        self.collisions: list[FRect] = []

        self.table: Table | None = None

        light: bool = False

        self.up_door: Door | None = None
        self.down_door: Door | None = None
        self.right_door: Door | None = None
        self.left_door: Door | None = None

        if randint(0, 2) == 0:
            self.table = Table()
            self.objects.append(self.table)

            if randint(0, 1) == 0:
                light = True
                self.objects.append(TableLamp())

        if not light:
            self.objects.append(Chandelier())

        # keep this method as small as possible, all the heavy load must be in static_loads and dynamic_loads

    def connect_to(self, other: Self):
        """Adds a door between two rooms"""
        assert (self.pos[0] == other.pos[0] or self.pos[1] == other.pos[1]) and (
                abs(self.pos[0] + self.pos[1] - other.pos[0] - other.pos[1]) == 1
        ), "rooms must be adjacent"
        from scripts.objects import Door

        # worse fucking code ever wrote in my life
        if self.pos[0] == other.pos[0]:
            if self.pos[1] < other.pos[1]:
                self.right_door = Door((0, self.size[1] // 2 - 0.01), True, True, other.pos)
                other.left_door = Door((0, - other.size[1] // 2 + 0.01), True, False, self.pos)
                self.objects.append(self.right_door)
                other.objects.append(other.left_door)
            else:
                self.left_door = Door((0, - self.size[1] // 2 + 0.01), True, False, other.pos)
                other.right_door = Door((0, other.size[1] // 2 - 0.01), True, True, self.pos)
                self.objects.append(self.left_door)
                other.objects.append(other.right_door)
        else:
            if self.pos[0] < other.pos[0]:
                self.up_door = Door((self.size[0] // 2 - 0.01, 0), False, True, other.pos)
                other.down_door = Door((- other.size[0] // 2 + 0.01, 0), False, False, self.pos)
                self.objects.append(self.up_door)
                other.objects.append(other.down_door)
            else:
                self.down_door = Door((- self.size[0] // 2 + 0.01, 0), False, False, other.pos)
                other.up_door = Door((other.size[0] // 2 - 0.01, 0), False, True, self.pos)
                self.objects.append(self.down_door)
                other.objects.append(other.up_door)

    def lock_door_to(self, pos: tuple[int, int]):
        if self.up_door is not None and self.up_door.destination == pos:
            self.up_door.locked = True
        elif self.down_door is not None and self.down_door.destination == pos:
            self.down_door.locked = True
        elif self.right_door is not None and self.right_door.destination == pos:
            self.right_door.locked = True
        elif self.left_door is not None and self.left_door.destination == pos:
            self.left_door.locked = True
        else:
            raise ValueError(
                f"The door to lock does not exist: {pos}\nAvailables: {(
                    None if self.up_door is None else self.up_door.destination,
                    None if self.down_door is None else self.down_door.destination,
                    None if self.right_door is None else self.right_door.destination,
                    None if self.left_door is None else self.left_door.destination
                )}"
            )

    def add_key(self):
        from scripts.objects import Key, SmallTable

        random_angle = random() * 2 * pi

        if self.table is None:
            distance = 2.5 * random()
            self.objects.append(SmallTable((cos(random_angle) * distance, sin(random_angle) * distance)))
            self.objects.append(Key((cos(random_angle) * distance, 0.8, sin(random_angle) * distance)))
        else:
            self.objects.append(Key((cos(random_angle) * 1.0, 0.9, sin(random_angle) * 1.0)))

    def static_loads(self):

        from scripts.objects import Door, Key
        door_count = len([o for o in self.objects if isinstance(o, Door)])
        key_count = len([o for o in self.objects if isinstance(o, Key)])
        if door_count == 1 and key_count == 0:
            print(f"Room {self.pos} has a door but no key")

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

        if randint(0, 3) > 0:
            carpet_sprite: Surface = random_choice(textures.carpets)
            carpet = textures.merge_carpet(carpet_sprite)
            floor.blit(carpet, (randint(22, floor.get_width() - 150), randint(22, floor.get_height() - 150)))

        self.scene.add_surface(floor, (-half_x, 0, -half_z), (half_x, 0, -half_z), (-half_x, 0, half_z))

        ceiling_sprite: Surface = random_choice(textures.ceilings)
        ceiling_texture = random_choice(textures.textures)
        ceiling: Surface = textures.repeat_layered(
            ceiling_sprite, self.size[0] // 2, self.size[1] // 2,
            ceiling_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        self.scene.add_surface(ceiling, (-half_x, y, -half_z), (-half_x, y, half_z), (half_x, y, -half_z))

        self.collisions.append(FRect(-x, -half_z, half_x, z))
        self.collisions.append(FRect(-half_x, -z, x, half_z))
        self.collisions.append(FRect(half_x, -half_z, half_x, z))
        self.collisions.append(FRect(-half_x, half_z, x, half_z))

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

    def get_collision(self) -> list[FRect]:

        collisions: list[FRect] = self.collisions.copy()

        for game_object in self.objects:
            collisions.extend(game_object.colliders)

        return collisions
