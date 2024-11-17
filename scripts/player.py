from typing import Final
from math import cos, sin, radians

from pygame import Vector3

from scripts import input_manager
from scripts.display import get_delta_time
from scripts import config

grid_position: tuple[int, int] = 0, 0
height: float = 1.3
position: Vector3 = Vector3()
angle_x: float = 0
angle_y: float = 90
fov: Final[float] = 90
speed: Final[float] = 2
jump_velocity: Final[float] = 3.5
current_vertical_velocity: float = 0


def move():
    global position, angle_x, angle_y, current_vertical_velocity

    rel = input_manager.get_relative_mouse_movement()

    angle_y -= rel[0] * config.mouse_speed
    angle_x -= rel[1] * config.mouse_speed

    angle_x = max(min(angle_x, 90), -90)

    delta_time: float = get_delta_time()

    current_speed = speed

    if position.y == height:
        if input_manager.crouch():
            position.y = 0.5
            current_speed /= 2
        elif input_manager.jump():
            current_vertical_velocity = jump_velocity
            position.y += current_vertical_velocity * delta_time
    else:
        if position.y < height:
            if not input_manager.crouch():
                position.y = height
                current_vertical_velocity = 0
        else:
            position.y += current_vertical_velocity * delta_time
            current_vertical_velocity -= 9.8 * delta_time

    horizontal = input_manager.horizontal_value() * delta_time * current_speed
    vertical = input_manager.vertical_value() * delta_time * current_speed

    position.x += vertical * cos(radians(angle_y)) + horizontal * cos(radians(angle_y + 90))
    position.z += vertical * sin(radians(angle_y)) + horizontal * sin(radians(angle_y + 90))
