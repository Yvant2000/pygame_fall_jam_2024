from typing import Final
from math import pow


def ease_out_back(x: float) -> float:
    c1: Final[float] = 1.70158
    c3: Final[float] = c1 + 1

    return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2)


def ease_out_bounce(x: float) -> float:
    n1: Final[float] = 7.5625
    d1: Final[float] = 2.75

    if x < 1 / d1:
        return n1 * x * x
    elif x < 2 / d1:
        x -= 1.5 / d1
        return n1 * x * x + 0.75
    elif x < 2.5 / d1:
        x -= 2.25 / d1
        return n1 * x * x + 0.9375
    else:
        x -= 2.625 / d1
        return n1 * x * x + 0.984375


def ease_out_expo(x: float) -> float:
    return 1 if x == 1 else 1.001 * (-pow(2, -10 * x) + 1)
