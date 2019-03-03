from models.tiles.dirt_tile import Dirt
from models.tiles.air_tile import Air
from models.tiles.stone_tile import Stone
from constants import TILE_SIZE_IN_PIXELS
from models.tiles.jeltisium_tile import Jeltisnium
from models.tiles.leninium_tile import Leninium
from models.tiles.marxinium_tile import Marxinium
from models.tiles.nokia_phonium_tile import NokiaPhonium
from models.tiles.half_liter_klokkium_tile import HalfLiterKlokkium
from constants import TILE_SIZE_IN_PIXELS, SCREEN_HEIGHT
import random
import bisect
import math
#values related to falling blocks
ADDSTAB_CUTOFF = 0.1
ROWS_UPDATED_PER_FRAME = 20
# These values are from above
DIRT_START = 20
STONE_START = 35
RESOURCE_START = 50

# Cap where the sigmoid function can decide the chance
RESOURCE_CHANCE_CAP = 0.25

# ratio peaks when resource is most common
resource_ratio_peaks = [None] * 5
resource_ratio_peaks[0] = [Jeltisnium, 0.15]
resource_ratio_peaks[1] = [Marxinium, 0.25]
resource_ratio_peaks[2] = [Leninium, 0.35]
resource_ratio_peaks[3] = [NokiaPhonium, 0.50]
resource_ratio_peaks[4] = [HalfLiterKlokkium, 0.90]

# to avoid magic numbers
RATIO_MAX = 1


class World(object):
    falling_tiles = []
    def __init__(self, width, height):
        """
        :param width: Width in tiles
        :param height: Height in tiles
        """
        self.tile_matrix = self.gen_world(width, height)
        self.width = width
        self.height = height
        self.row_counter = height - 1


    def gen_world(self, width, height):
        """
        Generate the world with some beautiful generation code
        :param width: width of the world
        :param height: height of the world
        :return: the generated world
        """
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
                # Are we below where the stone starts and above where the resources start?
                elif (y > STONE_START) and (y <= RESOURCE_START):
                    # Stone chance from sigmoid function
                    stone_chance = self.sigmoid(10 * (y / height) - 5)
                    if random.uniform(0, 1) > stone_chance:
                        column.append(Dirt(self, x, y, False))
                    else:
                        column.append(Stone(self, x, y))
                    continue
                # Are we below where the resources start?
                elif y > RESOURCE_START:
                    # Resource chance is from sigmoid function
                    resource_chance = self.sigmoid(10 * (y / height) - 7)
                    # To prevent suddenly everything being resources we cap where the sigmoid has influence
                    if resource_chance > RESOURCE_CHANCE_CAP:
                        # Here the resource chance becomes linear growing slowly
                        resource_chance = RESOURCE_CHANCE_CAP + (y / (height * 10))
                    if random.uniform(0, 1) < resource_chance:
                        # Use a separate function to decide the resource
                        column.append(self.decide_resource(x, y, height))
                        continue
                    # If we don't spawn a resource, just spawn stone using sigmoid to decide the chance
                    stone_chance = self.sigmoid(10 * (y / height) - 5)
                    if random.uniform(0, 1) > stone_chance:
                        column.append(Dirt(self, x, y, False))
                    else:
                        column.append(Stone(self, x, y))
                    continue
            world_matrix.append(column)
        return world_matrix

    def get_tile_at_indices(self, tile_x, tile_y):
        if tile_x < 0 or tile_y < 0:
            return None
        try:
            return self.tile_matrix[int(tile_x)][int(tile_y)]
        except IndexError:
            return None

    def set_tile_at_indices(self, tile_x, tile_y, tile):
        self.tile_matrix[int(tile_x)][int(tile_y)] = tile

    def get_tile_at(self, x, y):
        return self.get_tile_at_indices(x//TILE_SIZE_IN_PIXELS, y//TILE_SIZE_IN_PIXELS)

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
        """
        Function used for deciding which resource to spawn, don't ask me how it works
        :param weights: Array of weights, summing to 1
        :return: some result????
        """
        total = sum(weights)
        result = []
        cumsum = 0
        for w in weights:
            cumsum += w
            result.append(cumsum / total)
        return result

    def choice(self, population, weights):
        """
        Making a choice from a population and array of weights
        :param population: array of choices
        :param weights: array of weights corresponding to population summing to 1
        :return: the decided unit from population
        """
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

    @staticmethod
    def sigmoid(x):
        """
        Helper function for sigmoid
        :param x: the x
        :return: the result
        """
        return 1 / (1 + math.exp(-x))

    def draw(self, surface, camera_y):
        # Calculate bounds based on camera y to reduce lag drastically
        min_y = max(0, camera_y//TILE_SIZE_IN_PIXELS - 1)
        max_y = min(self.height, (camera_y + SCREEN_HEIGHT)//TILE_SIZE_IN_PIXELS + 1)

        for x in range(self.width):
            for y in range(min_y, max_y):
                self.tile_matrix[x][y].draw(surface, camera_y)

    def destroy_tile_on_indices(self, tile_x, tile_y):
        if self.get_tile_at_indices(tile_x, tile_y) is not None:
            self.tile_matrix[tile_x][tile_y] = Air(self, tile_x, tile_y)

    def destroy_tile(self, tile):
        self.destroy_tile_on_indices(tile.x, tile.y)

    def __repr__(self):
        s = ""
        for y in range(self.height):
            s += " | "
            for x in range(self.width):
                s += "%8s | "%str(self.tile_matrix[x][y])
            s += "\n"
        return s


    def update_should_fall(self):
        #for row in range(self.height - 1, 0, -1):
        for i in range(ROWS_UPDATED_PER_FRAME):
            for cell in range(self.width):
                self.get_tile_at_indices(cell, self.row_counter - 1).reset_stability()
            for cell in range(self.width):
                self.update_stabilities(cell, self.row_counter)
            for cell in range(self.width):
                if self.get_tile_at_indices(cell, self.row_counter - 1).check_stability():
                    self.falling_tiles.append(self.get_tile_at_indices(cell, self.row_counter - 1))
            self.row_counter -= 1
            if self.row_counter == 0:
                self.row_counter = self.height - 1

    def update_stabilities(self, x, y):
        source = self.get_tile_at_indices(x, y)
        if source.is_solid():
            startstabb = source.get_stability() * self.get_tile_at_indices(x, y - 1).get_strength()
            addstab = startstabb
            self.get_tile_at_indices(x, y - 1).update_stability(source.get_stability())
            i = 1
            while addstab > ADDSTAB_CUTOFF and i + x < self.width and i < 4:
                self.get_tile_at_indices(i + x, y - 1).update_stability(addstab)
                addstab *= self.get_tile_at_indices(i + x, y - 1).get_strength()
                i += 1
            addstab = startstabb
            i = -1
            while addstab > ADDSTAB_CUTOFF and x + i >= 0 and i > -4:
                self.get_tile_at_indices(x + i, y - 1).update_stability(addstab)
                addstab *= self.get_tile_at_indices(x + i, y - 1).get_strength()
                i -= 1


    def step(self):
        self.update_should_fall()
        i = 0
        while i < len(self.falling_tiles):
            tile = self.falling_tiles[i]
            if not tile.step():
                self.falling_tiles.remove(tile)
            else:
                i += 1

if __name__ == "__main__":
    world = World(64, 1024)
    print(world)
