#!/usr/bin/env python


from collections import deque

import numpy as np

from feh_simulator.action import Action
from feh_simulator.battle import attack
from feh_simulator.unit import Unit
from feh_simulator.skill import MovementType

# TODO: implement allies pass and enemy block in the reachable locations
class Map(object):
    def __init__(self, map_file='./map_data/map_default.txt'):
        with open(map_file) as f:
            content = f.readlines()
        self.nrows = int(content[0])
        self.ncols = int(content[1])

        self.terrain_grid = np.zeros(shape=(self.nrows, self.ncols), dtype=int)
        self.unit_grid = np.zeros(shape=(self.nrows, self.ncols), dtype=int)   # map to unitid

        for r in range(self.nrows):
            tmp = content[r + 2].split(' ')
            # check tmp length
            if len(tmp) != self.ncols:
                raise ValueError('Map data invalid.')
            self.terrain_grid[r] = tmp

        self.team_1_start_location = []
        self.team_2_start_location = []
        for r in range(self.nrows):
            tmp = content[r + 11].split(' ')
            for c in range(self.ncols):
                if int(tmp[c]) == 1:
                    self.team_1_start_location.append((c, r))
                elif int(tmp[c]) == 2:
                    self.team_2_start_location.append((c, r))
        return

    def register_unit(self, unit: Unit, x: int, y: int):
        if not self.is_location_standable(unit=unit, x=x, y=y):
            raise ValueError('Illegal initial location of unit:', unit.id)
        self.unit_grid[y, x] = unit.id
        unit.x = x
        unit.y = y

    def move_unit(self, unit: Unit, x: int, y: int):
        self.unit_grid[unit.y, unit.x] = 0
        self.unit_grid[y, x] = unit.id
        unit.x = x
        unit.y = y

    def remove_unit(self, x: int, y: int):
        self.unit_grid[y, x] = 0

    def is_location_standable(self, unit: Unit, x: int, y: int) -> bool:
        if x >= self.ncols or x < 0 or y >= self.nrows or y < 0:
            return False
        if self.terrain_grid[y, x] == 3:
            return False
        if self.terrain_grid[y, x] == 4:
            return False
        if self.terrain_grid[y, x] == 5:
            return False
        if self.terrain_grid[y, x] == 2 and unit.movement_type != MovementType.FLYING:
            return False
        if self.terrain_grid[y, x] == 1 and unit.movement_type == MovementType.CAVALRY:
            return False
        if self.unit_grid[y, x] != 0:  # if location is occupied (!= 0), then
            return False
        return True

    def get_reachable_locations(self, unit: Unit) -> {(int, int)}:
        """
        get all available movement target coordinates (before action on other units)
        :param unit:
        :return:
        """
        move_range = unit.get_movement_range(surrounding_units=set())
        reachable_coordinates: set = {(unit.x, unit.y)}
        visited_coordinates: set = set()
        pending_coordinates = deque([(unit.x, unit.y, move_range)], maxlen=self.ncols * self.nrows)
        while pending_coordinates:  # if it is not empty
            x, y, available_step = pending_coordinates.pop()
            visited_coordinates.add((x, y))
            if available_step == 0:
                continue
            if self.is_location_standable(unit=unit, x=x, y=y - 1):
                reachable_coordinates.add((x, y - 1))
                if (x, y - 1) not in visited_coordinates:
                    pending_coordinates.append((x, y - 1, available_step - 1))
            if self.is_location_standable(unit=unit, x=x - 1, y=y):
                reachable_coordinates.add((x - 1, y))
                if (x - 1, y) not in visited_coordinates:
                    pending_coordinates.append((x - 1, y, available_step - 1))
            if self.is_location_standable(unit=unit, x=x, y=y + 1):
                reachable_coordinates.add((x, y + 1))
                if (x, y + 1) not in visited_coordinates:
                    pending_coordinates.append((x, y + 1, available_step - 1))
            if self.is_location_standable(unit=unit, x=x + 1, y=y):
                reachable_coordinates.add((x + 1, y))
                if (x + 1, y) not in visited_coordinates:
                    pending_coordinates.append((x + 1, y, available_step - 1))
        return reachable_coordinates

    @staticmethod
    def get_distance(unit_a: Unit, unit_b: Unit):
        return abs(unit_a.x - unit_b.x) + abs(unit_a.y - unit_b.y)

    def find_units_by_distance(self, x: int, y: int, distance: int) -> set:
        found_unit_ids = set()
        for x0 in range(x - distance, x + distance + 1):
            for y0 in range(y - distance, y + distance + 1):
                if x0 < 0 or x0 >= self.ncols or y0 < 0 or y0>= self.nrows:
                    continue
                if abs(x0 - x) + abs(y0 - y) == distance:
                    if self.unit_grid[y0, x0] != 0:
                        found_unit_ids.add(self.unit_grid[y0, x0])
                else:
                    continue
        return found_unit_ids

    def render(self):
        for r in range(self.nrows):
            for c in range(self.ncols):
                print(self.terrain_grid[r, c], sep='', end=':')
                if self.unit_grid[r, c] >= 0:  # if the location is occupied by an unit, print the unit's id
                    print(self.unit_grid[r, c], sep='', end='  ')
                else:
                    print('_', sep='', end='  ')
            print('')
        return