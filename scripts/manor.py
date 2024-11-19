from typing import Final
from random import randrange, seed as set_random_seed

from scripts.room import Room
from scripts import player
from scripts.rooms import GoalRoom

grid_size: Final[tuple[int, int]] = 8, 8
rooms: list[list[Room | None]] = [[None for _ in range(grid_size[0])] for _ in range(grid_size[1])]
seed: int = randrange(999999999)


def init_manor():
    global seed
    set_random_seed(seed)
    rooms[0][1] = GoalRoom((0, 1))
    rooms[0][1].static_loads()


def run_manor():
    current_room: Room = rooms[player.grid_position[0]][player.grid_position[1]]
    if current_room is None:
        current_room = Room(player.grid_position)  # todo: generate room
        current_room.static_loads()
        rooms[player.grid_position[0]][player.grid_position[1]] = current_room

    current_room.dynamic_loads()
    current_room.handle_interactions()
    current_room.display()

    player.move(current_room.get_collision())
