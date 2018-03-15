#!/usr/bin/env python


import numpy as np

class Map(object):
    def __init__(self, ncols=6, nrows=8, nunits_a=4, nunits_b=4):
        self.ncols = ncols
        self.nrows = nrows
        self.map = np.array([[0,0,0,0,0,0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0]])
        self.friend_location = []
        self.enemry_location = []

    def get_action(unit):
        
        return

    def action(action):
        return

    def render();
        return