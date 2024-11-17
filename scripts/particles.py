from typing import Final
from random import random
from pygame import Vector2
from pygame.draw import circle
from scripts import display
from scripts.config import window_size


class Particle:

    def __init__(self, start_position: tuple[float, float]):
        self.start_position: tuple[float, float] = start_position
        self.position: Vector2 = Vector2()
        self.direction: Vector2 = Vector2()
        self.speed: float = 0
        self.size: float = 0
        self.remaining_lifetime: float = 0
        self.lifetime: float = 0

        self.init()

    def init(self):
        self.direction: Vector2 = Vector2(1, 0).rotate(random() * 360)
        self.position: Vector2 = Vector2(self.start_position) + self.direction * 300
        self.speed: float = random() * 250 + 50
        self.size: float = random() * 6 + 1
        self.lifetime: float = 3 * random() + 1
        self.remaining_lifetime: float = self.lifetime

    def update(self, delta_time: float):
        self.remaining_lifetime -= delta_time
        if self.remaining_lifetime <= 0:
            self.init()

        factor: float = (self.remaining_lifetime / self.lifetime)

        speed: float = self.speed * factor
        size: float = self.size * factor

        self.position += self.direction * speed * delta_time

        color: float = 255 * factor
        circle(display.window, (color, color, color), self.position, size)


amount: Final[int] = 50
particles: Final[list[Particle]] = [Particle((window_size[0] // 2, window_size[1] // 2)) for _ in range(amount)]


def update_particles(delta_time: float):
    for particle in particles:
        particle.update(delta_time)
