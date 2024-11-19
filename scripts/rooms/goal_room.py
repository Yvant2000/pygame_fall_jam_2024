from scripts.objects import EndingDoor, Chandelier
from scripts.room import Room


class GoalRoom(Room):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.objects = [EndingDoor(), Chandelier()]  # forget about default loads
