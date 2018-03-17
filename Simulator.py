from map import Map
from unit import Unit
import sys
from action import Action
class Simulator:
    def __init__(self, nrows=8, ncols=6):
        self.units = []
        self.row = nrows
        self.col = ncols
        self.map = Map(nrows, ncols, self.units)

    def create_unit(self, id, team):
    	unit = Unit(id, team)
    	self.unit.append(unit)

    def reset(self):
    	self.map = Map(self.row, self.col, self.units)
    	loc = self.map.get

    def step(self, a):
    	self.map.action(a)

def main(args):
	simu = Simulator()
	for i in range(8):
		create_unit(i, int(i / 4))
	action_space = simu.map.get_action_space(simu.units[2])
	action = action_space[3]
	print(action)
	simu.step(action)
	print(simu.map)

if __name__ == '__main__':
    main(sys.argv)
