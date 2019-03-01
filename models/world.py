import random

from models.tiles.dirt_tile import Dirt
from models.tiles.air_tile import Air
from models.tiles.stone_tile import Stone
from models.tiles.jeltisium_tile import Jeltisnium
from models.tiles.leninium_tile import Leninium
from models.tiles.marxinium_tile import Marxinium
from models.tiles.nokia_phonium_tile import NokiaPhonium
from models.tiles.half_liter_klokkium_tile import HalfLiterKlokkium
import random
import bisect
import collections


# These values are from above
DIRT_START = 20
STONE_START = 40
RESOURCE_START = 50

RESOURCE_CHANCE = 0.15

# ratio peaks when resource is most common
resource_ratio_peaks = [None] * 5
resource_ratio_peaks[0] = [Jeltisnium, 0.15]
resource_ratio_peaks[1] = [Marxinium, 0.25]
resource_ratio_peaks[2] = [Leninium, 0.35]
resource_ratio_peaks[3] = [NokiaPhonium, 0.50]
resource_ratio_peaks[4] = [HalfLiterKlokkium, 0.90]

# to avoid magic numbers
RATIO_MIN = 0
RATIO_MAX = 1


class World(object):

    def __init__(self, width, height):
        """
        :param width: Width in tiles
        :param height: Height in tiles
        """
        self.tile_matrix = self.gen_world(width, height)
        self.width = width
        self.height = height

    def gen_world(self, width, height):
        world_matrix = []
        for x in range(width):
            column = []
            for y in range(height):
                # Are we above where the ground starts?
                if y < DIRT_START:
                    column.append(Air(self, x, y))
                    continue
                # Are we where the ground start?
                elif y == DIRT_START:
                    column.append(Dirt(self, x, y, True))
                    continue
                # Are we below where the ground starts but above where the stone starts?
                elif (y > DIRT_START) and (y <= STONE_START):
                    column.append(Dirt(self, x, y, False))
                    continue
                # Are we below where the stone starts?
                elif (y > STONE_START) and (y <= RESOURCE_START):
                    stone_chance = y/height  # TODO: Sigmoid that shit
                    if random.uniform(0, 1) > stone_chance:
                        column.append(Dirt(self, x, y, False))
                    else:
                        column.append(Stone(self, x, y))
                    continue
                elif y > RESOURCE_START:
                    if random.uniform(0, 1) < RESOURCE_CHANCE:
                        column.append(self.decide_resource(x, y, height))
                        continue
                    stone_chance = y / height  # TODO: Sigmoid that shit
                    if random.uniform(0, 1) > stone_chance:
                        column.append(Dirt(self, x, y, False))
                    else:
                        column.append(Stone(self, x, y))
                    continue

            world_matrix.append(column)
        return world_matrix

    # hahaha lelijke functie dit eks dee ik wil dood
    def decide_resource(self, x, y, height):
        """
        Function used to decide which resource should be spawned in depending on how deep you are using
        resource_ratio_peaks to decide when what has what chance
        :param x: Only used for the return
        :param y: how deep you are
        :param height: the max height
        :return: Random resource depending on depth
        """
        distances = {}
        ratio_level = y / height
        for ratio_peak_list in resource_ratio_peaks:
            distances[ratio_peak_list[0]] = RATIO_MAX - abs(ratio_peak_list[1] - ratio_level)
        total_distances = 0
        for distance in distances.values():
            total_distances += distance
        normalized_chances = {}
        for distance in distances:
            normalized_chance = distances[distance] / total_distances
            normalized_chances[distance] = normalized_chance
        population = []
        weights = []
        for normalized_chance in normalized_chances:
            population.append(normalized_chance)
            weights.append(normalized_chances[normalized_chance])
        result = self.choice(population, weights)
        return result(self, x, y)

    def cdf(self, weights):
        total = sum(weights)
        result = []
        cumsum = 0
        for w in weights:
            cumsum += w
            result.append(cumsum / total)
        return result

    def choice(self, population, weights):
        assert len(population) == len(weights)
        cdf_vals = self.cdf(weights)
        x = random.random()
        idx = bisect.bisect(cdf_vals, x)
        return population[idx]

        # normalized_ratio_level = 2*((ratio_level - RATIO_MIN)/(RATIO_MAX - RATIO_MIN)) - 1
        # for ratio_peak in resource_ratio_peak:
        #     value = resource_ratio_peak[ratio_peak]
        #     normalized_ratio_peak = 2*((value - RATIO_MIN)/(RATIO_MAX - RATIO_MIN)) - 1
        #     chance = random.normalvariate(normalized_ratio_peak, 1)
        #     distances[ratio_peak] = chance
        #     print(ratio_peak, chance)
        # total_chance = sum(distances)
        # random.uniform(0, total_chance)







    def draw(self, surface, camera_y):
        for x in range(self.width):
            for y in range(self.height):
                self.tile_matrix[x][y].draw(surface, camera_y)

    def __repr__(self):
        s = ""
        for y in range(self.height):
            s += " | "
            for x in range(self.width):
                s += "%8s | "%str(self.tile_matrix[x][y])
            s += "\n"
        return s


if __name__ == "__main__":
    world = World(64, 1024)
    print(world)
