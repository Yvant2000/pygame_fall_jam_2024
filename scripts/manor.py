from typing import Final
from random import randrange, seed as set_random_seed, choice as random_choice, randint
from os.path import join as join_path

from pygame import Surface
from pygame.constants import SRCALPHA
from pygame.draw import rect as draw_rect
from pygame.transform import scale
from pygame.mixer import music

from scripts.room import Room
from scripts import player, display

grid_size: Final[int] = 8
rooms: list[list[Room]]
seed: int = randrange(999999999)
manor_map: Surface = Surface((grid_size * 4, grid_size * 4), flags=SRCALPHA)
discovered: list[list[bool]] = [[False for _ in range(grid_size)] for _ in range(grid_size)]
map_displayed: bool = True


def init_manor():
    global rooms
    from scripts.rooms import GoalRoom

    manor_map.fill((0, 0, 0, 0))

    global seed
    set_random_seed(seed)

    rooms = [[Room((j, i)) for i in range(grid_size)] for j in range(grid_size)]

    # 0 0 is the starting
    # 7 7 is the goal

    end_pos = (grid_size - 1, grid_size - 1)
    rooms[end_pos[0]][end_pos[1]] = GoalRoom((end_pos[0], end_pos[1]))

    length_matrix = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    marked_rooms: list[list[bool]] = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    graph: list[list[list[tuple[int, int]]]] = [[[] for _ in range(grid_size)] for _ in range(grid_size)]
    marked_rooms[0][0] = True
    available_rooms: list[tuple[int, int]] = [(0, 0)]
    created_rooms: int = 1

    # matrix of length from the start position

    while created_rooms < grid_size ** 2:
        # weight = length of the path from start / Manhattan distance to goal
        # we are looking for the available rooms with the smallest weight
        assert len(available_rooms) > 0, "No available rooms"

        min_weight = float('inf')
        min_rooms: list[tuple[int, int]] = []
        for room in available_rooms:  # type: tuple[int, int]
            weight: float = (
                float('inf') if room == end_pos
                else (length_matrix[room[0]][room[1]] - (room[0] + room[1]))
            )
            if weight < min_weight:
                min_weight = weight
                min_rooms = [room]
            elif weight == min_weight:
                min_rooms.append(room)

        # we have a room with the smallest weight
        room = random_choice(min_rooms)

        # we need to find the available neighbors
        neighbors = []
        if room[0] > 0 and not marked_rooms[room[0] - 1][room[1]]:
            neighbors.append((room[0] - 1, room[1]))
        if room[0] < grid_size - 1 and not marked_rooms[room[0] + 1][room[1]]:
            neighbors.append((room[0] + 1, room[1]))
        if room[1] > 0 and not marked_rooms[room[0]][room[1] - 1]:
            neighbors.append((room[0], room[1] - 1))
        if room[1] < grid_size - 1 and not marked_rooms[room[0]][room[1] + 1]:
            neighbors.append((room[0], room[1] + 1))

        if len(neighbors) == 0:
            available_rooms.remove(room)
            continue

        # we choose a random neighbor
        neighbor = random_choice(neighbors)
        marked_rooms[neighbor[0]][neighbor[1]] = True
        available_rooms.append(neighbor)
        length_matrix[neighbor[0]][neighbor[1]] = length_matrix[room[0]][room[1]] + 1
        created_rooms += 1

        rooms[room[0]][room[1]].connect_to(rooms[neighbor[0]][neighbor[1]])
        graph[room[0]][room[1]].append(neighbor)
        graph[neighbor[0]][neighbor[1]].append(room)

    # we visit all rooms and drop keys at dead ends
    marked_rooms = [[False for _ in range(grid_size)] for _ in range(grid_size)]
    available_rooms = [(0, 0)]
    available_keys: int = 0
    next_group: list[tuple[int, int]] = []
    current_group: list[tuple[int, int]] = []

    while len(available_rooms) > 0 or len(next_group) > 0:

        if len(available_rooms) == 0:

            # link all rooms in curent group
            for room_a in current_group:
                for room_b in current_group:
                    if ((room_a[0] == room_b[0] or room_a[1] == room_b[1])
                            and (abs(room_a[0] + room_a[1] - room_b[0] - room_b[1]) == 1)):
                        if randint(0, 3) > 0:
                            rooms[room_a[0]][room_a[1]].connect_to(rooms[room_b[0]][room_b[1]])

            available_rooms = next_group
            next_group = []
            current_group = []

        room = random_choice(available_rooms)
        available_rooms.remove(room)
        marked_rooms[room[0]][room[1]] = True
        current_group.append(room)

        # print(f"Handling {room}; {[r for r in graph[room[0]][room[1]] if not marked_rooms[r[0]][r[1]]]}")

        # todo groups
        if room != end_pos:
            neighbors = [r for r in graph[room[0]][room[1]] if not marked_rooms[r[0]][r[1]]]
            if len(neighbors) == 0:
                if randint(0, 2) == 0:
                    rooms[room[0]][room[1]].add_key()
                    available_keys += 1
                    # print(f"Drop Key in {room}")
            else:
                if available_keys > 0:
                    available_keys -= 1
                    neighbor_to_lock = random_choice(neighbors)
                    rooms[room[0]][room[1]].lock_door_to(neighbor_to_lock)
                    next_group.append(neighbor_to_lock)
                    neighbors.remove(neighbor_to_lock)

                for neighbor in neighbors:
                    available_rooms.append(neighbor)

    for list_rooms in rooms:  # type: list[Room]
        for room in list_rooms:  # type: Room
            room.static_loads()

    music.load(join_path("assets", "sounds", "an_empty_manor.mp3"))
    music.set_volume(0.5)
    music.play(-1)


def run_manor():
    current_room: Room = rooms[player.grid_position[0]][player.grid_position[1]]
    # if current_room is None:
    #     current_room = Room(player.grid_position)
    #     current_room.static_loads()
    #     rooms[player.grid_position[0]][player.grid_position[1]] = current_room

    current_room.dynamic_loads()
    current_room.handle_interactions()
    current_room.display()

    player.move(current_room.get_collision())
    draw_map()


def draw_map():
    discovered[player.grid_position[0]][player.grid_position[1]] = True

    for i in range(grid_size):
        for j in range(grid_size):
            if discovered[i][j]:
                draw_rect(manor_map, (150, 150, 150), (j * 4, i * 4, 3, 3))

    draw_rect(manor_map, (50, 50, 225), (player.grid_position[1] * 4, player.grid_position[0] * 4, 3, 3))
    if discovered[grid_size - 1][grid_size - 1]:
        draw_rect(manor_map, (50, 225, 50), ((grid_size - 1) * 4, (grid_size - 1) * 4, 3, 3))

    height: int = display.window_top_layer.get_height()
    map_height: int = height // 5
    rescaled_map: Surface = scale(manor_map, (map_height, map_height))

    if not map_displayed:
        return

    display.window_top_layer.blit(rescaled_map, (display.window_top_layer.get_width() - rescaled_map.get_width(), 0))
