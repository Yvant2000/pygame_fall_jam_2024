from typing import Final

from scripts.room import Room
from scripts import player

grid_size: Final[tuple[int, int]] = 8, 8
rooms: list[list[Room | None]] = [[None for _ in range(grid_size[0])] for _ in range(grid_size[1])]


def run_manor():
    current_room: Room = rooms[player.grid_position[0]][player.grid_position[1]]
    if current_room is None:
        current_room = Room()  # todo: generate room
        current_room.add_walls()
        rooms[player.grid_position[0]][player.grid_position[1]] = current_room

    current_room.dynamic_walls()
    current_room.display()

    player.move()
