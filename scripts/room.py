from random import choice as random_choice, randint

from pygame import Surface
from pysidocast import Scene
from scripts import player, textures, display


class Room:
    def __init__(self):
        self.scene = Scene()
        self.size: tuple[int, int] = 8, 8
        self.height: float = 4

        wall_index: int = randint(0, textures.wall_count - 1)
        wall_sprite: Surface = textures.merge_wall(textures.walls_bot[wall_index], textures.walls_top[wall_index])
        wall_texture: Surface = random_choice(textures.textures)

        self.wall_x: Surface = textures.repeat_layered(
            wall_sprite, self.size[0] // 2, 1, wall_texture, self.size[0] - 1, 3
        )
        self.wall_z: Surface = textures.repeat_layered(
            wall_sprite, self.size[1] // 2, 1, wall_texture, self.size[1] - 1, 3
        )

        floor_sprite: Surface = random_choice(textures.floors)
        floor_texture = random_choice(textures.textures)
        self.floor: Surface = textures.repeat_layered(
            floor_sprite, self.size[0] // 2, self.size[1] // 2, floor_texture, self.size[0] - 1, self.size[1] - 1
        )

        ceiling_sprite: Surface = random_choice(textures.ceilings)
        ceiling_texture = random_choice(textures.textures)
        self.ceiling: Surface = textures.repeat_layered(
            ceiling_sprite, self.size[0] // 2, self.size[1] // 2, ceiling_texture, self.size[0] - 1, self.size[1] - 1
        )

        self.light: Surface = random_choice(textures.lights)

    def add_walls(self):
        x = self.size[0]
        y: float = self.height
        z = self.size[1]
        half_x: float = x / 2
        half_z: float = z / 2

        self.scene.add_wall(self.wall_x, (-half_x, y, half_z), (half_x, 0, half_z))
        self.scene.add_wall(self.wall_x, (half_x, y, -half_z), (-half_x, 0, -half_z))
        self.scene.add_wall(self.wall_z, (half_x, y, -half_z), (half_x, 0, half_z))
        self.scene.add_wall(self.wall_z, (-half_x, y, half_z), (-half_x, 0, -half_z))

        self.scene.add_surface(self.floor, (-half_x, 0, -half_z), (half_x, 0, -half_z), (-half_x, 0, half_z))
        self.scene.add_surface(self.ceiling, (-half_x, y, -half_z), (-half_x, y, half_z), (half_x, y, -half_z))

        self.scene.add_wall(self.light, (-0.8, self.height, 0), (0.8, self.height - 1.6, 0))
        self.scene.add_wall(self.light, (0, self.height, -0.8), (0, self.height - 1.6, 0.8))

    def dynamic_walls(self): ...

    def display(self):
        self.scene.add_light((0, self.height, 0), intensity=4, direction=(0, 0, 0))  # room light
        self.scene.add_light(player.position, 2.5)  # player light
        self.scene.add_light((0, self.height - 0.8, 0))  # ceiling light

        self.scene.render(display.game_screen, player.position, player.angle_x, player.angle_y, player.fov, threads=-1)
        self.scene.clear_lights()
