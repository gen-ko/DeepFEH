from map import Map
from unit import Unit

class Simulator:
    def __init__(self, nrows=8, ncols=6):
        self.units = [Unit(int(i / 4), i) for i in range(8)]
        self.map = Map(nrows, ncols, self.units)

    def reset(self):
        return

    def step(self, a):

        return