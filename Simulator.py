from map import Map
from unit import Unit
import sys
from action import Action
class Simulator:
    def __init__(self, nrows=8, ncols=6):
        self.units = [Unit(int(i / 4), i) for i in range(8)]
        self.row = nrows
        self.col = ncols
        self.bmap = Map(nrows, ncols, self.units)

    def reset(self):
    	self.bmap = Map(self.row, self.col, self.units)

    def step(self, a):
    	self.bmap.action(a)

def main(args):
	simu = Simulator()
	action_space = simu.bmap.get_action_space(simu.units[0])
	for i, val in enumerate(action_space):
		print(type(val))
	action = Action(simu.units[0], [3,2], None)
	simu.step(action_space[0])

if __name__ == '__main__':
    main(sys.argv)
