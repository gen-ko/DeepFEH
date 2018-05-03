import sys
import random
from feh_simulator.session import Session

"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""


m2a = {0: (0, 2), 1: (-1, 1), 2: (0, 1), 3: (1, 1),
       4: (-2, 0), 5: (-1, 0), 6: (0, -2), 7: (1,0), 8:(2,0),
       9:(-1,-1), 10:(0, -1), 11:(1,-1), 12:(0, 0)}

a2m = {(0, 2): 0, (-1, 1): 1, (0, 1):2, (1, 1):3,
       (-2,0):4, (-1,0):5, (0, -2):6, (1,0):7, (2,0):8,
       (-1,-1):9, (0,-1):10, (1,-1):11, (0,0):12   }

class Simulator:
    def __init__(self, verbose=True, difficulty=1.0):
        self.verbose = verbose
        self.difficulty = difficulty
        self.session = None
        self.team = 1

    def create_unit(self,map_file='./map_data/map_01.txt',
                    unit_files=['./unit_data/unit03.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit02.txt',
                           './unit_data/unit02.txt',
                           './unit_data/unit02.txt',],
                    unit_teams=[1, 1, 1, 1, 2, 2, 2, 2]):
        """
        customize unit as you want
        """
        self.session = Session(map_file, unit_files, unit_teams)

    def get_action_space(self) -> [(int, int, int, int, int, int)]:
        """
        returns a list of actions that user can act 
        """
        actions = self.session.get_available_actions()
        ais = []
        for a in actions:
            ais.append(self._reverse_translate_action(a))
        return ais

    # Not finished
    def reset(self) -> ([int], int, bool):
        """
        Reset the FEH environment, returning current state, reward and done.
        """
        self.session.reset()
        state = self.session.current_state()
        reward = 0
        done, winner = self.session.is_session_end()
        return state, reward, done

    def _step(self, a:[int, int, int, int, int, int]) -> ([int], int, bool):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        switch = self.session.operate(a)
        state = self.session.current_state()
        reward = 0
        done, winner = self.session.is_session_end()
        if winner != -1:
            if winner == self.team:
                reward = 100
                return state, reward, done
            else:
                reward = -100
                return state, reward, done

        if switch:
            state, reward, done = self._AI()
        return state, reward, done
    
    
    def _translate_action(self, a:int) -> [int, int, int, int, int, int]:
        unit = self.session.units[a % 8] + 1
        x = unit.x
        y = unit.y
        dx, dy = m2a[int(a / 8) % 13]
        dtx, dty = m2a[int(a / 8 * 13)]
        return [x, y, dx, dy, dtx, dty]
    
    def _reverse_translate_action(self, a: [int, int, int, int, int, int]) -> int:
        unitid = self.map.unit_grid(a[1], a[0]) - 1
        d1 = a2m[(a[2], a[3])]
        d2 = a2m[(a[4], a[5])]
        return unitid + d1 * 8 + d2 * 8 * 13
        
    def step(self, a:int) -> ([int, int, bool, int]):
        x, y, dx, dy, dtx, dty = self._translate_action(a)
        return self._step([x, y, dx, dy, dtx, dty])

    def _AI(self):
        switch = False
        done = False
        reward = 0
        winner = -1
        while(not switch and not done):
            actions = self.session.get_available_actions()
            a = None
            if random.random() <= self.difficulty:
                for a_ in actions:
                    if a_[4] != 0 or a_[5] != 0:
                        a = a_
                        break
            if a is None:
                a = random.choice(actions)
            switch = self.session.operate(a)
            state = self.session.current_state()
            done, winner = self.session.is_session_end()
        if winner != -1:
            if winner == self.team:
                reward = 100
                return state, reward, done
            else:
                reward = -100
                return state, reward, done
        return state, reward, done

    def render(self):
        self.session.render()


def main(argv):
    simu = Simulator()
    simu.create_unit()
    s, r, done = simu.reset()
    print_info(simu, r, done)
    while not done:
        action = simu.get_action_space()
        a = None
        for a_ in action:
            if a_[4] != 0 or a_[5] != 0:
                a = a_
                break
        if a is None:
            a = random.choice(action)
        s, r, done = simu.step(a)
        # print_info(simu, r, done)
    print_info(simu, r, done)
    s, r, done = simu.reset()
    print_info(simu, r, done)
    while not done:
        action = simu.get_action_space()
        a = None
        for a_ in action:
            if a_[4] != 0 or a_[5] != 0:
                a = a_
                break
        if a is None:
            a = random.choice(action)
        s, r, done = simu.step(a)
        # print_info(simu, r, done)
    print_info(simu, r, done)


def print_info(simu, r, done):
    simu.session.render()
    print("reward is {}".format(r))
    print("session over? {}".format(done))


if __name__ == "__main__":
    main(sys.argv)