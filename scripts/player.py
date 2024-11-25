from typing import Final
from math import cos, sin, radians

from pygame import Vector3
from pygame.rect import FRect
from pysidocast import Scene

from scripts import input_manager, manor
from scripts.display import get_delta_time

grid_position: tuple[int, int] = 0, 0
height: float = 1.3
position: Vector3 = Vector3((-2, 1.3, -2))
movement_vector: Vector3 = Vector3()
angle_x: float = 0
angle_y: float = 45
fov: Final[float] = 90
speed: Final[float] = 2
jump_velocity: Final[float] = 3.5
mouse_speed: Final[float] = 0.1
reach: Final[float] = 1.7
key_count: int = 0


def move(collisions: list[FRect]):
    global position, angle_x, angle_y, movement_vector

    if input_manager.toggle_map():
        manor.map_displayed = not manor.map_displayed

    rel = input_manager.get_relative_mouse_movement()

    angle_y -= rel[0] * mouse_speed
    angle_x -= rel[1] * mouse_speed

    angle_x = max(min(angle_x, 90), -90)

    delta_time: float = get_delta_time()

    current_speed = speed

    if position.y < height:
        position.y = height

    if position.y > height:
        position += movement_vector * delta_time
        movement_vector.y -= 9.8 * delta_time
        rect = FRect(position.x - 0.3, position.z - 0.3, 0.6, 0.6)
        if rect.collidelist(collisions) != -1:
            position.x -= movement_vector.x * delta_time
            position.z -= movement_vector.z * delta_time
            movement_vector.x = movement_vector.z = 0
        return

    if input_manager.jump():
        movement_vector *= 1.2
        movement_vector.y = jump_velocity
        position += movement_vector * delta_time
        rect = FRect(position.x - 0.3, position.z - 0.3, 0.6, 0.6)
        if rect.collidelist(collisions) != -1:
            position.x -= movement_vector.x * delta_time
            position.z -= movement_vector.z * delta_time
            movement_vector.x = movement_vector.z = 0
        return

    if input_manager.crouch():
        position.y = 0.5
        current_speed /= 2

    horizontal = input_manager.horizontal_value()
    horizontal_vector = Vector3(cos(radians(angle_y + 90)), 0, sin(radians(angle_y + 90))) * horizontal * current_speed

    position += horizontal_vector * delta_time
    rect = FRect(position.x - 0.3, position.z - 0.3, 0.6, 0.6)
    if rect.collidelist(collisions) != -1:
        position -= horizontal_vector * delta_time

    vertical = input_manager.vertical_value()
    vertical_vector = Vector3(cos(radians(angle_y)), 0, sin(radians(angle_y))) * vertical * current_speed

    position += vertical_vector * delta_time
    rect = FRect(position.x - 0.3, position.z - 0.3, 0.6, 0.6)
    if rect.collidelist(collisions) != -1:
        position -= vertical_vector * delta_time

    movement_vector = horizontal_vector + vertical_vector


def get_pointer(scene: Scene) -> tuple[float, float, float]:
    distance = scene.single_cast(position, angle_x, angle_y, max_distance=reach)
    return (
        position.x + cos(radians(angle_y)) * distance * cos(radians(angle_x)),
        position.y + sin(radians(angle_x)) * distance,
        position.z + sin(radians(angle_y)) * distance * cos(radians(angle_x))
    )
