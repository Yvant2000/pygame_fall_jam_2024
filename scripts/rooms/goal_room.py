from scripts.objects import EndingDoor
from scripts.room import Room


class GoalRoom(Room):
    def __init__(self, pos: tuple[int, int]):
        super().__init__(pos)
        self.up_door = self.right_door = EndingDoor()
        self.objects.append(self.up_door)
