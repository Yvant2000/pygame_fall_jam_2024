from abc import ABC, abstractmethod
from random import choice as random_choice

from pygame import Surface

from pysidocast import Scene

import textures


class Props(ABC):
    def static_load_surfaces(self, scene: Scene):
        """Called once when creating a room. \n
        Useful to load static images when creating a scene
        """

    def dynamic_load_surfaces(self, scene: Scene):
        """Called every frame when the player is in the room \n
        Useful to display temporary surfaces depending on the context
        """


class Door(Props):
    def __init__(self):
        self.texture: Surface = random_choice(textures.doors)


