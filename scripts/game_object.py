from abc import ABC, abstractmethod

from pygame.locals import Rect

from scripts.room import Room


class GameObject(ABC):
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
        return False

    def interact(self):
        """Interact with the object"""
        return
