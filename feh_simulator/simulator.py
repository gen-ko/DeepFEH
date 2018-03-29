import copy
import random
import sys

from feh_simulator.map import Map
from feh_simulator.unit import Unit

"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""


class Simulator:
    def __init__(self, nrows=8, ncols=6, verbose=True, difficulty=0.0):
        self.verbose = verbose
        self.nrows = nrows
        self.ncols = ncols
        self.units = []
        self.units_backup = []
        self.map = Map(self.nrows, self.ncols, self.units, self.verbose)
        self.friendly_round = []
        self.enemy_round = []
        self.difficulty = difficulty

    def create_unit(self, id, team, max_hp=40):
        """
        customize unit that you want
        """
        unit = Unit(id, team, max_hp=max_hp)
        self.units.append(unit)
        self.units_backup.append(copy.deepcopy(unit))
        if team == 0:
            self.friendly_round.append(unit)
        if team == 1:
            self.enemy_round.append(unit)

    def reset(self):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        self.units = copy.deepcopy(self.units_backup)
        self.map = Map(self.nrows, self.ncols, self.units, self.verbose)
        loc = self.map.get_locations()

        # refill the round list
        self.friendly_round = []
        self.enemy_round = []
        for i, val in enumerate(self.units):
            if val.team == 0:
                self.friendly_round.append(val)
            if val.team == 1:
                self.enemy_round.append(val)

        return loc, 0, False

    def step(self, a):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        reward = 0
        unit = a.src_unit
        self.friendly_round.remove(unit)
        loc, done, dead = self.map.action(a)
        if done:
            if self.verbose:
                print("last dead unit is {}".format(dead.index))
            if dead.team == 0:
                reward = -100
                if self.verbose:
                    print("Enemy wins, you suck")
            else:
                reward = 100
                if self.verbose:
                    print("You win, you rock")
            return loc, reward, done
        self._update_list(dead)

        # if friendly units finish moveing, let enemy move
        if len(self.friendly_round) == 0:
            loc, reward, done = self._opponent_move()
        return loc, reward, done

    def get_action_space(self):
        """
        returns a list of actions that user can act next
        """
        space = []
        for i, val in enumerate(self.friendly_round):
            tmp_space = self.map.get_action_space(val)
            space.extend(tmp_space)
        return space

    def _opponent_move(self):
        """
        stupid opponent moves
        """
        # opponent moves randomly
        grid = []
        reward = -1
        done = False
        for i, val in enumerate(self.enemy_round):
            action = self.map.get_action_space(val)
            a = None
            if random.random() <= self.difficulty:
                for a_ in action:
                    if a_.des_unit is not None:
                        a = a_
                        break
            if a is None:
                a = random.choice(action)
            grid, done, dead = self.map.action(a)
            if done:
                if self.verbose:
                    print("last dead unit is {} ".format(dead.index))
                if dead.team == 0:
                    reward = -100
                    if self.verbose:
                        print("Enemy wins, you suck")
                else:
                    reward = 100
                    if self.verbose:
                        print("You win, you rock")
                return grid, reward, done
            self._update_list(dead)

        # refill the friendly round list
        for i, val in enumerate(self.units):
            if val.team == 0:
                self.friendly_round.append(val)
        return grid, reward, done

    def _update_list(self, dead):
        """
        update the list to remove the dead unit
        """
        if dead is None:
            return

        self.units.remove(dead)
        if dead.team == 0:
            if dead in self.friendly_round:
                self.friendly_round.remove(dead)
        if dead.team == 1:
            self.enemy_round.remove(dead)


def main(argv):
    simu = Simulator()
    for i in range(8):
        simu.create_unit(i, int(i / 4))
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
        # print_info(s, r, done)
    print_info(s, r, done)
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
        # print_info(s, r, done)
    print_info(s, r, done)


def print_info(s, r, done):
    print(s)
    print(r)
    print(done)


if __name__ == "__main__":
    main(sys.argv)