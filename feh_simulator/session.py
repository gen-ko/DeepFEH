import copy
import random
import sys

from feh_simulator.map import Map
from feh_simulator.unit import Unit
import feh_simulator.battle as battle

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
        self.active_unit_ids = []
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
        remove_list = []
        for unit_id, unit in self.units.items():
            if not unit.is_alive:
                remove_list.append((unit_id, unit))
                
        for unit_id, unit in remove_list:
            self.map.remove_unit(unit.x, unit.y)
            self.units.pop(unit_id)
        return

    def operate(self, action: (int, int, int, int, int, int)):

        source_unit_x: int = action[0]
        source_unit_y: int = action[1]
        dx: int = action[2]
        dy: int = action[3]
        target_unit_dx: int = action[4]
        target_unit_dy: int = action[5]

        source_unit_id = self.map.unit_grid[source_unit_y, source_unit_x]
        source_unit = self.units[source_unit_id]
        self.map.move_unit(source_unit, x=source_unit.x + dx, y=source_unit.y + dy)

        if target_unit_dx == 0 and target_unit_dy == 0:
            return
        target_unit_id = self.map.unit_grid[target_unit_dy + source_unit.y, 
                                            target_unit_dx + source_unit.x]
        
        target_unit = self.units[target_unit_id]
        battle.act(source_unit, target_unit)
        self.active_unit_ids.remove(source_unit_id)
        # clear dead units
        self.clear_units()

        if self.active_unit_ids.__len__ == 0:  # if active units list is empty
            if self.current_turn == 1:
                self.current_turn = 2
                self.activate_team(team_id=2)
            elif self.current_turn == 2:
                self.current_turn = 1
                self.activate_team(team_id=1)
                self.current_round += 1
        return

    def get_available_actions(self) -> [(int, int, int, int, int, int)]:
        """

        :return: [source_unit_id, dx, dy, target_unit_id]
        """
        action_list: [(int, int, int, int, int, int)] = []
        for unit_id in self.active_unit_ids:
            unit = self.units[unit_id]
            reachable_locations = self.map.get_reachable_locations(unit)
            for (x, y) in reachable_locations:
                # stand by
                action_list.append((unit.x, unit.y, x - unit.x, y - unit.y, 0, 0))
                # attack
                target_unit_ids = self.map.find_units_by_distance(x=x, y=y, distance=unit.attack_range)
                for target_id in target_unit_ids:
                    target_unit = self.units[target_id]
                    if target_unit.team == unit.team:
                        continue
                    target_dx = target_unit.x - x
                    target_dy = target_unit.y - y
                    action_list.append((unit.x, unit.y, x - unit.x, y - unit.y, 
                                        target_dx,
                                        target_dy))
                # support
                """
                target_unit_ids = self.map.find_units_by_distance(x=x, y=y, distance=unit.support_range)
                for target_id in target_unit_ids:
                    target_unit = self.units[target_id]
                    if target_unit.team != unit.team:
                        continue
                    target_dx = target_unit.x - x
                    target_dy = target_unit.y - y
                    action_list.append((unit.x, unit.y, x - unit.x, y - unit.y, 
                                        target_dx,
                                        target_dy))
                """
        return action_list

    def is_session_end(self) ->  (bool, int):
        # return the id of the winner team
        winner_id = -1
        for _, unit in self.units.items():
            if winner_id == -1:
                winner_id = unit.team
            if unit.team != winner_id:
                return False, -1
        return True, winner_id
    
    def current_state(self) -> []:
        state = [self.map.terrain_grid.flat, self.map.unit_grid.flat]
        for _, unit in self.units.items():
            state.append(unit.get_attributes())
        for _ in range(8 - self.units.__len__()):
            state.append([0, 0, 0, 0, 0,   0, 0, 0, 0,0,   0, 0, 0, 0])
        return [item for sublist in state for item in sublist]
    
    def render(self):
        self.map.render()
