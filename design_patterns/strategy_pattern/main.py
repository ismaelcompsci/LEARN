from abc import ABC, abstractmethod

from matplotlib.pyplot import vlines
from tomlkit import value


class FilterStrategy(ABC):
    @abstractmethod
    def removeValue(self, val):
        pass


# Implemantation to remove all negative values
class RemoveNegativeStrategy(FilterStrategy):
    def removeValue(self, val):
        return val < 0


# Implemantation to remove all odd values
class RemoveOddStrategy(FilterStrategy):
    def removeValue(self, val):
        return abs(val) % 2


class Values:
    def __init__(self, vals):
        self.vals = vals

    def filter(self, strategy):
        res = []

        for n in self.vals:
            if not strategy.removeValue(n):
                res.append(n)

        return res


values = Values([-4, -3, -2, 0, 2, 4, 5])

print(values.filter(RemoveNegativeStrategy()))  # [0, 2, 4, 5]
print(values.filter(RemoveOddStrategy()))  # [-4, -2, 0, 2, 4]
