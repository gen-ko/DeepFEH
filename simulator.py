from map import Map
from unit import Unit


class Simulator:
    def __init__(self, nrows=8, ncols=6):
        self.nrows = nrows
        self.ncols = ncols
        self.units = None
        self.map = None
        self.counter = None

    def reset(self):
        """
        Reset the FEH environment, returning current locations, friendly team positions, enemy team locations, and unit attributes.
        :return: A vector denoting unit attributes and a 2D matrix denoting unit positions.
        """
        self.units = [Unit(i, int(i / 4)) for i in range(8)]
        self.map = Map(self.nrows, self.ncols, self.units)
        self.counter = 0
        positions = self.map.get_locations()
        attributes = [unit.get_attributes() for unit in self.units]
        action_space = [self.map.get_action_space(unit) for unit in self.units if unit.team == 0]
        return positions, attributes, action_space

    def step(self, a):
        self.map.action(a)
        positions = self.map.get_locations()
        attributes = [unit.get_attributes() for unit in self.units]
        action_space = [self.map.get_action_space(unit) for unit in self.units if unit.team == 0]
        self.counter = (self.counter + 1) % 4
        if self.counter == 0:
            self.opponent_move()
        return positions, attributes, action_space

    def opponent_move(self):
        print("Opponent move")
