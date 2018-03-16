from map import Map
from unit import Unit

class Simulator:
    def __init__(self, nrows=8, ncols=6):
        self.units = [Unit(int(i / 4), i) for i in range(8)]
        self.row = nrows
        self.col = ncols
        self.map = Map(nrows, ncols, self.units)

    def reset(self):
    	self.map = Map(self.row, self.col, self.units)
        return

    def step(self, action):
    	self.map(action)
        return

def main(args):

if __name__ == '__main__':
    main(sys.argv)
