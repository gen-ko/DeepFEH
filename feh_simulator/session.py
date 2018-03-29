import copy
import random
import sys

from feh_simulator.map import Map
from feh_simulator.unit import Unit
import feh_simulator.battle as battle
"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""


class Session:
    def __init__(self, map_file: str, unit_files: [str], unit_teams: [int]):
        self.map_file = map_file
        self.unit_files = unit_files
        self.unit_teams = unit_teams
        self.map = None
        self.units = {}
        self.current_turn = 0
        self.current_round = 0
        self.active_unit_ids: [int] = []
        self.reset()
        return

    def reset(self):
        self.map = Map(map_file=self.map_file)
        team1_start_location = self.map.team_1_start_location
        team2_start_location = self.map.team_2_start_location
        self.units = {}
        Unit.reset()
        for i, unit_file in enumerate(self.unit_files):
            team = self.unit_teams[i]
            u = Unit(team=team, unit_file=unit_file)
            if team == 1:
                x, y = team1_start_location.pop(0)
            elif team == 2:
                x, y = team2_start_location.pop(0)
            self.map.register_unit(unit=u, x=x, y=y)
            self.units[u.id] = u
        self.current_turn = 1  # 1 : team 1 turn,  2 : team 2 turn
        self.current_round = 1
        self.activate_team(team_id=self.current_turn)
        return

    def activate_team(self, team_id: int):
        for unit_id, unit in self.units.items():
            if unit.team == team_id:
                self.active_unit_ids.append(unit_id)

    def clear_units(self):
        for unit_id, unit in self.units.items():
            if unit.is_dead:
                self.map.remove_unit(unit.x, unit.y)
                self.units.pop(unit_id)
        return

    def operate(self, source_unit_id, dx, dy, target_unit_id):
        source_unit = self.units[source_unit_id]
        self.map.move_unit(source_unit, x=source_unit.x + dx, y=source_unit.y + dy)
        target_unit = self.units[target_unit_id]
        battle.act(source_unit, target_unit)
        self.active_unit_ids.remove(source_unit_id)
        # clear dead units
        self.clear_units()

        if not self.active_unit_ids:  # if active units list is empty
            if self.current_turn == 1:
                self.current_turn = 2
                self.activate_team(team_id=2)
            if self.current_turn == 1:
                self.current_turn = 1
                self.activate_team(team_id=1)
                self.current_round += 1
        return

    def get_available_actions(self) -> [(int, int, int, int)]:
        """

        :return: [source_unit_id, dx, dy, target_unit_id]
        """
        action_list: [(int, int, int, int)] = []
        for unit_id, unit in self.units.items():
            reachable_locations = self.map.get_reachable_locations(unit)
            for (x, y) in reachable_locations:
                # attack
                target_unit_ids = self.map.find_units_by_distance(x=x, y=y, distance=unit.attack_range)
                for target_id in target_unit_ids:
                    if self.units[target_id].team == unit.team:
                        continue
                    action_list.append((unit_id, x - unit.x, y - unit.y, target_id))
                # support
                target_unit_ids = self.map.find_units_by_distance(x=x, y=y, distance=unit.support_range)
                for target_id in target_unit_ids:
                    if self.units[target_id].team != unit.team:
                        continue
                    action_list.append((unit_id, x - unit.x, y - unit.y, target_id))
        return action_list