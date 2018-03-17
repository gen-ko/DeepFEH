#!/usr/bin/env python


from collections import deque

import numpy as np

from action import Action
from battle import attack


class Map:
    def __init__(self, nrows=8, ncols=6, units=None):
        self.nrows = nrows
        self.ncols = ncols
        self.units = units
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
        while queue:
            (x, y), distance = queue.popleft()
            move_destinations.add((x, y))
            dx = [0, 0, 1, -1]
            dy = [1, -1, 0, 0]
            for k in range(4):
                x_, y_ = x + dx[k], y + dy[k]
                if (x_,
                    y_) not in move_destinations and 0 <= x_ <= self.nrows - 1 and 0 <= y_ <= self.ncols - 1 and distance + 1 <= unit.move_range and \
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

    def _get_enemies(self, unit):
        return [candidate for candidate in self.units if candidate.team != unit.team]

    def get_locations(self):
        friends_map = np.array([[0 for _ in range(self.ncols)] for _ in range(self.nrows)])
        friends = [position for unit, position in self.locations.items() if unit.team == 0]
        for x, y in friends:
            friends_map[x][y] = 1
        enemy_map = np.array([[0 for _ in range(self.ncols)] for _ in range(self.nrows)])
        enemies = [position for unit, position in self.locations.items() if unit.team == 1]
        for x, y in enemies:
            enemy_map[x][y] = 1
        return friends_map, enemy_map

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

        # attack enemy
        if action.des_unit is not None:
            attack(action.src_unit, action.des_unit)

            # delete from locations
            if action.src_unit.is_dead:
                x, y = self.locations[action.src_unit]
                del self.locations[action.src_unit]
                self.grid[x][y] = 0

            if action.des_unit.is_dead:
                x, y = self.locations[action.des_unit]
                del self.locations[action.des_unit]
                self.grid[x][y] = 0

    def render(self):
        print("Vacancy grid is ")
        print(self.grid)
