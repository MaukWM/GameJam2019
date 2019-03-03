from abc import ABC, abstractmethod
FALLING_THRESHOLD = 0.25
STEPS_TO_FALL = 2

class Tile(ABC):
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.stability = 1
        self.isfalling = False
        self.strength = self.get_initial_strength()
        self.health = 1
        self.fallcounter = 0
        self.solid = True

    def can_support(self):
        return True

    @abstractmethod
    def draw(self, surface, camera_y):
        pass

    @abstractmethod
    def is_solid(self) -> bool:
        pass

    def get_initial_strength(self):
        return 0

    @abstractmethod
    def get_resistance(self):
        pass

    def get_strength(self):
        return self.strength

    def damage(self, amount):
        if self.get_strength() == 0.0:
            return False
        self.health -= amount / self.get_resistance()
        if self.health <= 0:
            return True             # it breaks
        else:
            return False            # it doesn't break

    def __repr__(self):
        return str(self.__class__.__name__)

    def get_stability(self):
        return self.stability

    def update_stability(self, incrementation):
        if self.is_solid():
            self.stability += incrementation
            if self.stability > 1:
                self.stability = 1

    def reset_stability(self):
        self.stability = 0

    def check_stability(self):
        if self.isfalling:
            return False
        if self.stability < FALLING_THRESHOLD:
            self.isfalling = True
            return True
        return False

    def step(self):
        if self.isfalling:
            if self.fallcounter < STEPS_TO_FALL:
                self.fallcounter += 1
                return True
            else:
                self.fallcounter = 0
                if not self.world.get_tile_at_indices(self.x, self.y + 1).can_support():
                    self.world.set_tile_at_indices(self.x, self.y, self.world.get_tile_at_indices(self.x, self.y + 1))
                    self.world.get_tile_at_indices(self.x, self.y).y -= 1
                    self.y += 1
                    self.world.set_tile_at_indices(self.x, self.y, self)
                    return True
                else:
                    self.isfalling = False
                    return False

