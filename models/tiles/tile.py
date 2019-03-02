from abc import ABC, abstractmethod


class Tile(ABC):
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.stability = 1
        self.should_fall = False

    @abstractmethod
    def draw(self, surface, camera_y):
        pass

    @abstractmethod
    def is_solid(self) -> bool:
        pass

    @abstractmethod
    def get_strength(self):
        pass

    def damage(self, amount):
        if self.get_strength() == 0.0:
            return False

        self.stability -= amount / self.get_strength()
        if self.stability <= 0:
            return True             # it breaks
        else:
            return False            # it doesn't break

    def __repr__(self):
        return str(self.__class__.__name__)
