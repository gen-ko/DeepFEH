#!/usr/bin/env python


import numpy as np
from unit import Unit

class Map(object):
    def __init__(self, ncols=6, nrows=8, nunits_a=4, nunits_b=4):
        self.ncols = ncols
        self.nrows = nrows
        self.is_blocked = np.array([[0,0,0,0,0,0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.units_a = {Unit(): (0, 0), Unit(): (1, 0), Unit(): (2, 0), Unit(): (3, 0)}
        self.units_b = {Unit(): {0, 7}, Unit(): (1, 7), Unit(): (2, 7), Unit(): (3, 8)}

    def get_action(self, a: Unit):
        location = self.units


    def move(self, a: Unit):

    def movable(self, a: Unit):
