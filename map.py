#!/usr/bin/env python


import numpy as np

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
        self.units_a = {(0,0): None, (0,0):None, (0,0):None, (0,0): None}
        self.units_b = {(0,0): None, (0,0):None, (0,0):None, (0,0): None}

    def