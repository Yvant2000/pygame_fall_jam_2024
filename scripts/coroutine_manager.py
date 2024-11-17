from typing import Generator


class Coroutine:
    def __init__(self, coroutine: Generator):
        self.coroutine: Generator = coroutine
        self.wait: float | None = next(self.coroutine)

    def update(self, delta_time: float) -> bool:
        """Update the coroutine.
        :param delta_time: The time in seconds to wait before the next update.
        :return: True if the coroutine is done, False otherwise.
        """
        if self.wait is not None and self.wait > 0:
            self.wait -= delta_time
            return False

        try:
            self.wait = next(self.coroutine)
        except StopIteration:
            return True

        return False


coroutines: list[Coroutine] = []


def create_coroutine(enumerator: Generator):
    coroutines.append(Coroutine(enumerator))


def update_coroutines(delta_time: float):
    for coroutine in coroutines.copy():
        if coroutine.update(delta_time):
            coroutines.remove(coroutine)
