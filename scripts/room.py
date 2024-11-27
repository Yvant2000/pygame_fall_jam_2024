from random import choice as random_choice, randint, random
from math import pi, cos, sin
from typing import Self

from pygame import Surface
from pygame.rect import FRect
from pygame.transform import rotate

from pysidocast import Scene

from scripts import player, textures, display, input_manager


class Room:
    def __init__(self, pos: tuple[int, int]):
        from scripts.game_object import GameObject
        from scripts.objects import Table, TableLamp, Door, TableOrnement

        self.pos: tuple[int, int] = pos
        self.scene = Scene()
        self.size: tuple[int, int] = 8, 8
        self.height: float = 4
        self.objects: list[GameObject] = []
        self.pos: tuple[int, int]
        self._loaded: bool = False
        self.collisions: list[FRect] = []

        self.table: GameObject | None = None
        self.light: GameObject | None = None

        self.up_door: Door | None = None
        self.down_door: Door | None = None
        self.right_door: Door | None = None
        self.left_door: Door | None = None

        if randint(0, 2) == 0:
            self.table = Table()
            self.objects.append(self.table)

            if randint(0, 1) == 0:
                self.light = TableLamp()
                self.objects.append(self.light)
            elif randint(0, 3) != 0:
                self.objects.append(TableOrnement((0, 0.85, 0)))

    def connect_to(self, other: Self):
        """Adds a door between two rooms"""
        assert (self.pos[0] == other.pos[0] or self.pos[1] == other.pos[1]) and (
                abs(self.pos[0] + self.pos[1] - other.pos[0] - other.pos[1]) == 1), "rooms must be adjacent"
        from scripts.objects import Door

        # some of the worse fucking code ever wrote in my life
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
                f"The door to lock does not exist: {pos}\nAvailables: "
                f"{(self.up_door.destination if self.up_door is not None else None, self.down_door.destination if self.down_door is not None else None, self.right_door.destination if self.right_door is not None else None, self.left_door.destination if self.left_door is not None else None)}"
            )

    def add_key(self):
        from scripts.objects import Key, SmallTable, LeatherChair, Plant

        random_angle = random() * 2 * pi

        if self.table is None:
            distance = 0.5 + 1.0 * random()
            self.table = SmallTable((cos(random_angle) * distance, sin(random_angle) * distance))
            self.objects.append(self.table)
            self.objects.append(Key((cos(random_angle) * distance, 0.8, sin(random_angle) * distance)))
            self.objects.append(LeatherChair((cos(random_angle + pi) * 1, sin(random_angle + pi) * 1)))
            distance += 0.5 * random()
            self.objects.append(Plant((cos(random_angle + pi / 2) * distance, sin(random_angle + pi / 2) * distance)))
        else:
            self.objects.append(Key((cos(random_angle) * 1.0, 0.9, sin(random_angle) * 1.0)))

    def static_loads(self):
        from scripts.objects import RoomCenter, Chandelier, Pillar, Plant, WoodenChair, SmallTable, Bookshelf, \
            TableOrnement, TableLamp, LeatherChair, Key, George, Table, Closet, Clock
        fill_center: bool = self.table is None and randint(0, 3) == 0

        if randint(0, 4) == 0:
            self.objects.append(Pillar((-3, -3)))
        elif randint(0, 4) == 0:
            self.objects.append(Plant((-3, -3)))

        if randint(0, 4) == 0:
            self.objects.append(Pillar((3, -3)))
        elif randint(0, 4) == 0:
            self.objects.append(Plant((3, -3)))

        if randint(0, 4) == 0:
            self.objects.append(Pillar((-3, 3)))
        elif randint(0, 4) == 0:
            self.objects.append(Plant((-3, 3)))

        if randint(0, 4) == 0:
            self.objects.append(Pillar((3, 3)))
        elif randint(0, 4) == 0:
            self.objects.append(Plant((3, 3)))

        if self.light is None:
            self.light = Chandelier()
            self.objects.append(self.light)

        wall_index: int = randint(0, textures.wall_count - 1)
        wall_sprite: Surface = textures.merge_wall(textures.walls_bot[wall_index], textures.walls_top[wall_index])
        wall_texture: Surface = random_choice(textures.textures)

        wall_x1: Surface = textures.repeat_layered(
            wall_sprite, self.size[0] // 2, 1, wall_texture, self.size[0] // 2 - 1, 3
        )
        wall_x2 = wall_x1.copy()
        wall_z1: Surface = textures.repeat_layered(
            wall_sprite, self.size[1] // 2, 1, wall_texture, self.size[1] // 2 - 1, 3
        )
        wall_z2 = wall_z1.copy()

        if fill_center:
            x_surf = Surface((wall_x1.get_width() // 4, wall_x1.get_height())).convert_alpha()
            x_surf.blit(wall_x1, (0, 0))
            z_surf = Surface((wall_z1.get_width() // 4, wall_z1.get_height())).convert_alpha()
            z_surf.blit(wall_z1, (0, 0))
            self.objects.append(RoomCenter(x_surf, z_surf))
        else:
            if self.table is None:
                # some hardcoded positions
                position: int = randint(0, 42)
                match position:
                    case 0:
                        self.objects.append(SmallTable((0.0, 0.0), pi / 4))
                        self.objects.append(TableOrnement((0.0, 0.7, 0.0)))
                        self.objects.append(WoodenChair((1.0, 0.0), 3 * pi / 4))
                        self.objects.append(WoodenChair((-1.0, 0.0), -pi / 4))
                        self.objects.append(WoodenChair((0.0, 1.0), -3 * pi / 4))
                        self.objects.append(WoodenChair((0.0, -1.0), pi / 4))
                        self.objects.append(Pillar((1., 1.)))
                        self.objects.append(Pillar((-1., 1.)))
                        self.objects.append(Pillar((1., -1.)))
                        self.objects.append(Pillar((-1., -1.)))
                    case 1:
                        x = randint(-2, 2)
                        z = randint(-2, 2)
                        self.objects.append(WoodenChair((x, z)))
                        self.objects.append(TableLamp((x, 0.65, z)))
                        self.objects.remove(self.light)
                    case 2:
                        for i in range(10):
                            for j in range(10):
                                if randint(0, 1) == 0:
                                    self.objects.append(TableOrnement((-3 + i * 2 / 3, 0.0, -3 + j * 2 / 3)))
                    case 3:
                        self.objects.append(WoodenChair((0, -1), -3 * pi / 4))
                        self.objects.append(TableOrnement((0, 0.7, -1)))
                        self.objects.append(LeatherChair((-2, 0.25), 175))
                        self.objects.append(LeatherChair((-1, 0.75), 150))
                        self.objects.append(LeatherChair((0, 1), 90))
                        self.objects.append(LeatherChair((1, 0.75), 60))
                        self.objects.append(LeatherChair((2, 0.25), 25))
                    case 4:
                        self.objects.append(WoodenChair((0, 2.0), -3 * pi / 4))
                        self.objects.append(WoodenChair((0, -2.0), pi / 4))
                        for i in range(7):
                            self.objects.append(Pillar((-2 + i * 2 / 3, 0)))
                    case 5:
                        self.objects.append(WoodenChair((0, 0.0), 0))
                        self.objects.append(WoodenChair((0, 0.0), -3 * pi / 4, height=0.50))
                        self.objects.append(WoodenChair((0, 0.0), 3 * pi / 4, height=1.1))
                        self.objects.append(TableLamp((0, 1.8, 0.0)))
                        self.objects.remove(self.light)
                    case 6:
                        self.objects.append(Plant((0, 0.0)))
                        self.objects.append(TableOrnement((1.0, 0.0, 0.0)))
                        self.objects.append(TableOrnement((1.0, 0.0, 1.0)))
                        self.objects.append(TableOrnement((0.0, 0.0, 1.0)))
                        self.objects.append(TableOrnement((-1.0, 0.0, 1.0)))
                        self.objects.append(TableOrnement((-1.0, 0.0, 0.0)))
                        self.objects.append(TableOrnement((-1.0, 0.0, -1.0)))
                        self.objects.append(TableOrnement((0.0, 0.0, -1.0)))
                        self.objects.append(TableOrnement((1.0, 0.0, -1.0)))
                    case 7:
                        self.objects.append(Key((0, 0, 0)))
                        self.objects.append(SmallTable((0, 0.0)))
                        self.objects.append(Pillar((0.9, 0.0)))
                        self.objects.append(Pillar((0.9, 0.9)))
                        self.objects.append(Pillar((0.0, 0.9)))
                        self.objects.append(Pillar((-0.9, 0.9)))
                        self.objects.append(Pillar((-0.9, 0.0)))
                        self.objects.append(Pillar((-0.9, -0.9)))
                        self.objects.append(Pillar((0.0, -0.9)))
                        self.objects.append(Pillar((0.9, -0.9)))
                    case 8:
                        self.objects.append(WoodenChair((0, -2.0), pi / 3))
                        self.objects.append(WoodenChair((0, 2.0), -2 * pi / 3))
                        self.objects.append(WoodenChair((2.0, 0.0), 2 * pi / 3))
                        self.objects.append(WoodenChair((-2.0, 0.0), -pi / 3))
                        self.objects.append(George((0, 0.65, -2.0)))
                        self.objects.append(Table())
                        self.objects.append(TableOrnement((0, 0.7, 0)))
                    case _:
                        if randint(0, 1) == 0:
                            pos = random() * 1 - 0.5, random() * 1 - 0.5
                            self.objects.append(SmallTable(pos))
                            if randint(0, 1) == 0:
                                self.objects.append(TableOrnement((pos[0], 0.7, pos[1])))
                        if randint(0, 1) == 0:
                            distance = 0.8 + 0.7 * random()
                            angle = random() * 2 * pi
                            self.objects.append(WoodenChair((cos(angle) * distance, sin(angle) * distance)))
                        if randint(0, 1) == 0:
                            distance = 0.8 + 0.7 * random()
                            angle = random() * 2 * pi
                            self.objects.append(LeatherChair((cos(angle) * distance, sin(angle) * distance)))
                        if randint(0, 1) == 0:
                            distance = 1.5 + 1 * random()
                            angle = random() * 2 * pi
                            self.objects.append(Plant((cos(angle) * distance, sin(angle) * distance)))

            elif not isinstance(self.table, SmallTable):
                for i in range(1, 5):
                    if randint(0, i) == 0:
                        distance = 1.4 + 0.4 * random()
                        angle = random() * 2 * pi
                        self.objects.append(WoodenChair((cos(angle) * distance, sin(angle) * distance)))

        for i in range(4):
            if randint(0, i + 3) == 0:
                wall = random_choice((wall_x1, wall_x2, wall_z1, wall_z2))
                poster = random_choice(textures.posters)
                poster_rot = rotate(poster, randint(-25, 25))
                wall.blit(
                    poster_rot, (randint(0, wall.get_width() - poster_rot.get_width()),
                                 randint(0, wall.get_height() - poster_rot.get_height() - 20))
                )

        x = self.size[0]
        y: float = self.height
        z = self.size[1]
        half_x: float = x / 2
        half_z: float = z / 2

        self.scene.add_wall(wall_x1, (-half_x, y, half_z), (half_x, 0, half_z))
        self.scene.add_wall(wall_x2, (half_x, y, -half_z), (-half_x, 0, -half_z))
        self.scene.add_wall(wall_z1, (-half_x, y, -half_z), (-half_x, 0, half_z))
        self.scene.add_wall(wall_z2, (half_x, y, half_z), (half_x, 0, -half_z))

        floor_sprite: Surface = random_choice(textures.floors)
        floor_texture = random_choice(textures.textures)
        floor: Surface = textures.repeat_layered(
            floor_sprite, self.size[0] // 2, self.size[1] // 2,
            floor_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        if not fill_center and randint(0, 3) == 0:
            trapdoor = random_choice(textures.trapdoors)
            trapdoor_rot = rotate(trapdoor, randint(0, 360))
            floor.blit(
                trapdoor_rot, (randint(0, floor.get_width() - trapdoor_rot.get_width()),
                               randint(0, floor.get_height() - trapdoor_rot.get_height()))
            )

        if not fill_center and randint(0, 3) > 0:
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

        if randint(0, 8) == 0:
            self.objects.append(Closet((-4, -2), 1))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((-4, -2), 1))
        if randint(0, 8) == 0:
            self.objects.append(Closet((-4, 2), 1))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((-4, 2), 1))
        if randint(0, 8) == 0:
            self.objects.append(Closet((4, -2), 3))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((4, -2), 3))
        if randint(0, 8) == 0:
            self.objects.append(Closet((4, 2), 3))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((4, 2), 3))
        if randint(0, 8) == 0:
            self.objects.append(Closet((-2, -4), 2))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((-2, -4), 2))
        if randint(0, 8) == 0:
            self.objects.append(Closet((2, -4), 2))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((2, -4), 2))
        if randint(0, 8) == 0:
            self.objects.append(Closet((-2, 4), 0))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((-2, 4), 0))
        if randint(0, 8) == 0:
            self.objects.append(Closet((2, 4), 0))
        elif randint(0, 8) == 0:
            self.objects.append(Clock((2, 4), 0))

        if self.down_door is None:
            if randint(0, 3) != 0:
                self.objects.append(Bookshelf(-self.size[0] // 2 + 0.01, False))
            if randint(0, 10) == 0:
                self.objects.append(Closet((-4, 0), 1))
            elif randint(0, 10) == 0:
                self.objects.append(Clock((-4, 0), 1))
        if self.up_door is None:
            if randint(0, 3) != 0:
                self.objects.append(Bookshelf(self.size[0] // 2 - 0.01, False))
            if randint(0, 10) == 0:
                self.objects.append(Closet((4, 0), 3))
            elif randint(0, 10) == 0:
                self.objects.append(Clock((4, 0), 3))
        if self.left_door is None:
            if randint(0, 3) != 0:
                self.objects.append(Bookshelf(-self.size[1] // 2 + 0.01, True))
            if randint(0, 10) == 0:
                self.objects.append(Closet((0, -4), 2))
            elif randint(0, 10) == 0:
                self.objects.append(Clock((0, -4), 2))
        if self.right_door is None:
            if randint(0, 3) != 0:
                self.objects.append(Bookshelf(self.size[1] // 2 - 0.01, True))
            if randint(0, 10) == 0:
                self.objects.append(Closet((0, 4), 0))
            elif randint(0, 10) == 0:
                self.objects.append(Clock((0, 4), 0))

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
