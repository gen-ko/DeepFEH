#!/usr/bin/env python


import numpy as np
from unit import Unit

class Map(object):
    def __init__(self, nrows=8, ncols=6, nunits_a=4, nunits_b=4):
        self.ncols = ncols
        self.nrows = nrows
        self.grid = np.array([[0 for c in range(ncols)] for r in range(nrows)])
        self.location = {}

        self.battle = 

    def get_action(self, unit):
        # dfs get all possible location that can go
        def dfs(i, j, loc, row, col, res):
            if i >= row or j >= col:
                return
            res.append([i,j])
            dfs(i+1,j,row,col,res)
            dfs(i-1,j,row,col,res)
            dfs(i,j+1,row,col,res)
            dfs(i,j-1,row,col,res)
            return
        res = []
        loc = self.location[unit]
        dfs(loc[0],loc[1],self.nrows, self.ncols)
        # iteration to see if there is some enemy that can attack
        

        return res

    def action(self, action):
        if action.src_unit in location:
            location[action.src_unit] = self.destination

        if self.des_unit is not None:
            self.battle(action.src_unit, action.des_unit)

        if action.src_unit.is_dead:
            del location[action.src_unit]

        if action.des_unit.is_dead:
            del location[action.des_unit]

        return

    def render(self);
        return

class Action(obejct):
    def __init__(self, unit):
        self.src_unit = None
        self.des_unit = None
        self.destination = []

