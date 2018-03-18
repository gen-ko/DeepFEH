#!/usr/bin/env python


from collections import deque

import numpy as np

from action import Action
from battle import attack


class Map:
    def __init__(self, nrows=8, ncols=6, units=None):
        self.verbose = True
        self.nrows = nrows
        self.ncols = ncols
        self.units = units
        self.done = False
        self.grid = np.array([[0 for _ in range(ncols)] for _ in range(nrows)])
        self.locations = {
            unit: [i % 2 if i < 4 else nrows - 1 - (i - 4) % 2, int(i / 2) if i < 4 else ncols - 1 - int((i - 4) / 2)]
            for i, unit in enumerate(units, 0)}
        for x, y in self.locations.values():
            self.grid[x][y] = 1

    def get_action_space(self, unit):
        loc = self.locations[unit]

        # get all move destinations
        move_destinations = set([])
        queue = deque(maxlen=self.nrows * self.ncols)
        queue.append((loc, 0))
        move_destinations.add(tuple(loc))
        dx = [0, 0, 1, -1]
        dy = [1, -1, 0, 0]
        while queue:
            (x, y), distance = queue.popleft()
            move_destinations.add((x, y))
            for k in range(4):
                x_, y_ = x + dx[k], y + dy[k]
                if (x_,
                    y_) not in move_destinations and 0 <= x_ <= self.nrows - 1 and 0 <= y_ <= self.ncols - 1 and distance + 1 <= unit.movement_range and \
                        self.grid[x_][y_] != 1:
                    queue.append(([x_, y_], distance + 1))

        # get all attack enemies and construct possible actions
        res = []
        for move_dest in move_destinations:
            # don't attack -> des_unit is None
            res.append(Action(unit, move_dest, None))
            for enemy in self._get_enemies(unit):
                if self._get_distance(move_dest, self.locations[enemy]) <= unit.attack_range:
                    # attack -> des_uniut is enemy
                    res.append(Action(unit, move_dest, enemy))
        return res

    # modified unit to location because if return element in unit, the for loop just above will have error
    def _get_enemies(self, unit):
        return [candidate for candidate in self.locations if candidate.team != unit.team]

    def _get_friendly(self, unit):
        return [candidate for candidate in self.locations if candidate.team == unit.team]

    def get_locations(self):
        loc = np.array([[0 for _ in range(self.ncols)] for _ in range(self.nrows)])
        friends = [position for unit, position in self.locations.items() if unit.team == 0]
        enemies = [position for unit, position in self.locations.items() if unit.team == 1]
        for x, y in friends:
            loc[x][y] = 1
        for x, y in enemies:
            loc[x][y] = 1
        return loc

    @staticmethod
    def _get_distance(pos_a, pos_b):
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

    def action(self, action):
        # move source unit
        if action.src_unit in self.locations:
            x_, y_ = action.destination
            x, y = self.locations[action.src_unit]
            self.locations[action.src_unit] = x_, y_
            self.grid[x][y] = 0
            self.grid[x_][y_] = 1
            if self.verbose:
                print("unit " + str(action.src_unit.index) + " move to " + str(x_) + "," + str(y_))

        dead = None
        # attack enemy
        if action.des_unit is not None:
            attack(action.src_unit, action.des_unit)
            if self.verbose:
                print("unit " + str(action.src_unit.index) + " attack " + str(action.des_unit.index))

            # delete from locations
            if action.src_unit.is_dead:
                x, y = self.locations[action.src_unit]
                del self.locations[action.src_unit]
                self.grid[x][y] = 0
                dead = action.src_unit

            if action.des_unit.is_dead:
                x, y = self.locations[action.des_unit]
                del self.locations[action.des_unit]
                self.grid[x][y] = 0
                dead = action.des_unit

        done = False
        if len(self._get_friendly(action.src_unit)) == 0 or len(self._get_enemies(action.src_unit)) == 0:
            done = True
        return self.grid, done, dead

    def set_verbose(self, v):
        self.verbose = v

    def __str__(self):
        return str(self.grid)

    def render(self):
        print("Vacancy grid is ")
        print(self.grid)
