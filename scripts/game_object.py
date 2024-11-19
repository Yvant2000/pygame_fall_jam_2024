from abc import ABC, abstractmethod

from pygame import Surface
from pygame.locals import Rect
from pygame.constants import BLEND_RGB_ADD, BLEND_RGB_SUB

from scripts.room import Room


class GameObject(ABC):
    def __init__(self, position: tuple[float, float, float] = (0, 0, 0)):
        self.position: tuple[float, float, float] = position
        self.buffer: Surface | None = None
        self._is_lighted: bool = False
        self.is_interactable: bool = False

    @abstractmethod
    def static_load(self, room: Room):
        """Loads all static surfaces in the scene"""
        ...

    @property
    def colliders(self) -> list[Rect]:
        """Returns all colliders in the object"""
        return []

    def dynamic_load(self, room: Room):
        """Loads all dynamic surfaces and chandelier in the scene"""
        return

    def can_interact(self, player_pointer: tuple[float, float, float]) -> bool:
        """Returns whether the object can be interacted with
        :param player_pointer: The player's pointer position
        :return: True if the object can be interacted with
        """
        if not self.is_interactable:
            return False

        assert self.buffer is not None, "buffer where not initialized"

        color: tuple[int, int, int] = (50, 50, 25)

        if Vector3_distance(self.position, player_pointer) < 0.8:
            if not self._is_lighted:
                self.buffer.fill(color, special_flags=BLEND_RGB_ADD)
                self._is_lighted = True
            return True
        else:
            if self._is_lighted:
                self.buffer.fill(color, special_flags=BLEND_RGB_SUB)
                self._is_lighted = False
            return False

    def interact(self):
        """Interact with the object"""
        assert self.is_interactable
        return


def Vector3_distance(a: tuple[float, float, float], b: tuple[float, float, float]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5
