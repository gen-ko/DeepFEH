import copy
import random
import sys

from feh_simulator.map import Map
from feh_simulator.unit import Unit
from feh_simulator.battle import *
from feh_simulator.action import Action

"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""



class Simulator:
    def __init__(self, verbose=True, difficulty=1.0):
        self.verbose = verbose
        self.units = []
        self.units_backup = []
        self.map = Map()
        self.friendly_round = []
        self.enemy_round = []
        self.difficulty = difficulty

    def create_unit(self, team, x, y):
        """
        customize unit as you want
        """
        unit = Unit(team)
        unit.x = x
        unit.y = y
        self.units.append(unit)
        self.units_backup.append(copy.deepcopy(unit))
        self.map.register_unit(unit, x, y)
        if team == 0:
            self.friendly_round.append(unit)
        if team == 1:
            self.enemy_round.append(unit)

    def _get_unit_by_id(self, id) -> Unit:
        """
        get unit instance by its id
        """
        for i in self.units:
            if i.id == id:
                return i

    def _get_unit_action_space(self, unit) -> list:
        """
        get the unit action space
        """
        action = []
        reachable = self.map.get_reachable_locations(unit)
        for loc in reachable:
            a = Action(unit, loc, None)
            action.append(a)
            attack_ids = self.map.find_units_by_distance(loc[0], loc[1], unit.attack_range)
            for unit_id in attack_ids:
                attackee = self._get_unit_by_id(unit_id)
                if attackee.team != unit.team:
                    new_attack = Action(unit, loc, attackee)
                    action.append(new_attack)
        return action

    def _remove_unit(self, unit):
        """
        remove the unit from all lists and map
        """
        self.units.remove(unit)
        for u in self.friendly_round:
            if u == unit:
                self.friendly_round.remove(unit)
        for u in self.enemy_round:
            if u == unit:
                self.enemy_round.remove(unit)
        self.map.remove_unit(unit.x, unit.y)

    # Not finished
    def _action(self, a):
        """
        execute the action
        """
        self.map.move_unit(a.src_unit, a.destination[0], a.destination[1])
        if a.des_unit is not None:
            attack(a.src_unit, a.des_unit)
        # update the list and map to remove the dead unit
        dead = None
        if a.src_unit.is_dead:
            dead = a.src_unit
            self._remove_unit(a.src_unit)
        if a.des_unit is not None and a.des_unit.is_dead:
            dead = a.des_unit
            self._remove_unit(a.des_unit)

        friendly_num = 0
        enemy_num = 0
        for u in self.units:
            if u.team == 0:
                friendly_num += 1
            else:
                enemy_num += 1
        done = False
        if friendly_num == 0 or enemy_num == 0:
            done = True
        # Not defined yet
        state = None
        return state, done, dead


    def get_action_space(self):
        """
        returns a list of actions that user can act 
        """
        space = []
        for i, val in enumerate(self.friendly_round):
            tmp_space = self._get_unit_action_space(val)
            space.extend(tmp_space)
        return space

    # Not finished
    def reset(self):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        self.units = copy.deepcopy(self.units_backup)
        self.map = Map()
        for u in self.units:
            self.map.register_unit(u, u.x, u.y)

        # Not defined yet 
        state = None
        # refill the round list
        self.friendly_round = []
        self.enemy_round = []
        for i, val in enumerate(self.units):
            if val.team == 0:
                self.friendly_round.append(val)
            if val.team == 1:
                self.enemy_round.append(val)

        return state, 0, False

    def step(self, a):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        reward = 0
        unit = a.src_unit
        self.friendly_round.remove(unit)
        state, done, dead = self._action(a)
        if done:
            if self.verbose:
                print("last dead unit is {}".format(dead.id))
            if dead.team == 0:
                reward = -100
                if self.verbose:
                    print("Enemy wins, you suck")
            else:
                reward = 100
                if self.verbose:
                    print("You win, you rock")
            return state, reward, done

        # if friendly units finish moveing, let enemy move
        if len(self.friendly_round) == 0:
            state, reward, done = self._opponent_move()
        return state, reward, done

    def _opponent_move(self):
        """
        stupid opponent moves
        """
        # opponent moves randomly
        grid = []
        reward = -1
        done = False
        for i, val in enumerate(self.enemy_round):
            action = self._get_unit_action_space(val)
            a = None
            if random.random() <= self.difficulty:
                for a_ in action:
                    if a_.des_unit is not None:
                        a = a_
                        break
            if a is None:
                a = random.choice(action)
            grid, done, dead = self._action(a)
            if done:
                if self.verbose:
                    print("last dead unit is {} ".format(dead.id))
                if dead.team == 0:
                    reward = -100
                    if self.verbose:
                        print("Enemy wins, you suck")
                else:
                    reward = 100
                    if self.verbose:
                        print("You win, you rock")
                return grid, reward, done

        # refill the friendly round list
        for i, val in enumerate(self.units):
            if val.team == 0:
                self.friendly_round.append(val)
        return grid, reward, done

def main(argv):
    simu = Simulator()
    simu.create_unit(team=0, x=0, y=0)
    simu.create_unit(team=1, x=4, y=4)
    s, r, done = simu.reset()
    print_info(simu, r, done)
    while not done:
        action = simu.get_action_space()
        print(action)
        a = None
        for a_ in action:
            if a_.des_unit is not None:
                a = a_
                break
        if a is None:
            a = random.choice(action)
        s, r, done = simu.step(a)
        print_info(simu, r, done)
        # print_info(simu, r, done)
    print_info(simu, r, done)
    s, r, done = simu.reset()
    while not done:
        action = simu.get_action_space()
        a = None
        for a_ in action:
            if a_.des_unit is not None:
                a = a_
                break
        if a is None:
            a = random.choice(action)
        s, r, done = simu.step(a)
        # print_info(simu, r, done)
    print_info(simu, r, done)


def print_info(simu, r, done):
    simu.map.render()
    print(r)
    print(done)


if __name__ == "__main__":
    main(sys.argv)