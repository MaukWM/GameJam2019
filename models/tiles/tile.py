from abc import ABC, abstractmethod


class Tile(ABC):
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, surface, camera_y):
        pass

    @abstractmethod
    def is_solid(self) -> bool:
        pass

    def __repr__(self):
        return str(self.__class__.__name__)
