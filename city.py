# city.py
import math

class City:
    def __init__(self, x, y, package_weight):
        self.x = x
        self.y = y
        self.package_weight = package_weight

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)