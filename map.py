#!/usr/bin/env python


import numpy as np

from battle import attack
from unit import Unit
from collections import deque


class Map:
    def __init__(self, nrows=8, ncols=6, units=None):
        units = [Unit(int(i / 4), i) for i in range(8)]
        self.nrows = nrows
        self.ncols = ncols
        self.units = units
        self.grid = np.array([[0 for _ in range(ncols)] for _ in range(nrows)])
        self.locations = {
        unit: [int(i / 2) if i < 4 else ncols - 1 - int((i - 4) / 2), i % 2 if i < 4 else nrows - 1 - (i - 4) % 2] for
        i, unit in enumerate(units, 0)}
        for x, y in self.locations.values():
            self.grid[x][y] = 1

    def get_action(self, unit):
        loc = self.locations[unit]
        # get all destinations
        move_destinations = []
        queue = deque(maxlen=self.nrows * self.ncols)
        queue.append(loc, 0)
        while queue:
            (x, y), distance = queue.popleft()
            move_destinations.append((x, y))
            dx = [0, 0, 1, -1]
            dy = [1, -1, 0, 0]
            for k in range(4):
                x_, y_ = x + dx[k], y + dy[k]
                if 0 <= x_ <= self.nrows - 1 and 0 <= y_ <= self.ncols and distance + 1 <= unit.move_range:
                    queue.append((x_, y_), distance + 1)

        # iteration to see if there is some enemy that can attack
        res = []
        for move_dest in move_destinations:
            # don't attack -> des_unit is None
            res.append(Action(unit, move_dest, None))
            for enemy in self.get_enemies(unit):
                if self.get_distance(unit, enemy) <= unit.attack_range:
                    # attack -> des_uniut is enemy
                    res.append(Action(unit, move_dest, enemy))

        return res

    def get_enemies(self, unit):
        return [candidate for candidate in self.units if candidate.team != unit.team]

    def get_distance(self, unit_a, unit_b):
        return abs(self.locations[unit_a][1] - self.locations[unit_b][1]) + abs(self.locations[unit_a][2] - self.locations[unit_b][2])

    def action(self, action):
        # move source unit
        if action.src_unit in self.locations:
            self.locations[action.src_unit] = action.destination

        # attack enemy
        if action.des_unit is not None:
            attack(action.src_unit, action.des_unit)

        # delete from locations
        if action.src_unit.is_dead:
            del self.locations[action.src_unit]
            x, y = self.locations[action.src_unit]
            self.grid[x][y] = 0

        if action.des_unit.is_dead:
            del self.locations[action.des_unit]
            x, y = self.locations[action.des_unit]
            self.grid[x][y] = 0

    def render(self):
        print("Grid is ")
        print(self.grid)


class Action:
    def __init__(self, src_unit, destination, des_unit):
        self.src_unit = src_unit
        self.des_unit = des_unit
        self.destination = destination
