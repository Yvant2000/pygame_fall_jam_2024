from random import choice as random_choice, randint

from pygame import Surface
from pysidocast import Scene
from scripts import player, textures, display, input_manager


class Room:
    def __init__(self, pos: tuple[int, int]):
        from scripts.game_object import GameObject
        from scripts.objects import Chandelier, Door

        self.scene = Scene()
        self.size: tuple[int, int] = 8, 8
        self.height: float = 4
        self.objects: list[GameObject] = [Chandelier(), Door((0, 0, 3.99), True, (pos[0], pos[1] + 1))]
        self.pos: tuple[int, int]

        wall_index: int = randint(0, textures.wall_count - 1)
        wall_sprite: Surface = textures.merge_wall(textures.walls_bot[wall_index], textures.walls_top[wall_index])
        wall_texture: Surface = random_choice(textures.textures)

        self.wall_x: Surface = textures.repeat_layered(
            wall_sprite, self.size[0] // 2, 1, wall_texture, self.size[0] // 2 - 1, 3
        )
        self.wall_z: Surface = textures.repeat_layered(
            wall_sprite, self.size[1] // 2, 1, wall_texture, self.size[1] // 2 - 1, 3
        )

        floor_sprite: Surface = random_choice(textures.floors)
        floor_texture = random_choice(textures.textures)
        self.floor: Surface = textures.repeat_layered(
            floor_sprite, self.size[0] // 2, self.size[1] // 2,
            floor_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        ceiling_sprite: Surface = random_choice(textures.ceilings)
        ceiling_texture = random_choice(textures.textures)
        self.ceiling: Surface = textures.repeat_layered(
            ceiling_sprite, self.size[0] // 2, self.size[1] // 2,
            ceiling_texture, self.size[0] // 2 - 1, self.size[1] // 2 - 1
        )

        for game_object in self.objects:
            game_object.static_load(self)

    def add_walls(self):
        x = self.size[0]
        y: float = self.height
        z = self.size[1]
        half_x: float = x / 2
        half_z: float = z / 2

        self.scene.add_wall(self.wall_x, (-half_x, y, half_z), (half_x, 0, half_z))
        self.scene.add_wall(self.wall_x, (half_x, y, -half_z), (-half_x, 0, -half_z))
        self.scene.add_wall(self.wall_z, (-half_x, y, -half_z), (-half_x, 0, half_z))
        self.scene.add_wall(self.wall_z, (half_x, y, half_z), (half_x, 0, -half_z))

        self.scene.add_surface(self.floor, (-half_x, 0, -half_z), (half_x, 0, -half_z), (-half_x, 0, half_z))
        self.scene.add_surface(self.ceiling, (-half_x, y, -half_z), (-half_x, y, half_z), (half_x, y, -half_z))

    def dynamic_walls(self):
        for game_object in self.objects:
            game_object.dynamic_load(self)

    def handle_interactions(self):
        player_pointer = player.get_pointer(self.scene)
        for game_object in self.objects:
            if game_object.can_interact(player_pointer):
                if input_manager.click():
                    game_object.interact()
                break

    def display(self):
        self.scene.add_light(player.position, 2.5)  # player light

        render_distance: float = (self.size[0] ** 2 + self.size[1] ** 2) ** 0.5  # gives more depth to the scene

        self.scene.render(
            display.game_screen, player.position, player.angle_x, player.angle_y, player.fov, threads=-1,
            view_distance=render_distance
        )
        self.scene.clear_lights()
