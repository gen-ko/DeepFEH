import random
import sys

from feh_simulator.session import Session

"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""


class Simulator:
    def __init__(self, verbose=True, difficulty=1.0, max_steps=200):
        self.verbose = verbose
        self.difficulty = difficulty
        self.session = None
        self.team = 1
        self.num_steps = 0
        self.max_steps = max_steps

    def create_unit(self, map_file='/Users/shijiewu/github/DeepFEH/feh_simulator/map_data/map_default.txt',
                    unit_files=['/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt',
                                '/Users/shijiewu/github/DeepFEH/feh_simulator/unit_data/unit_default.txt', ],
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
        return actions

    # Not finished
    def reset(self) -> ([int], int, bool):
        """
        Reset the FEH environment, returning current state, reward and done.
        """
        self.session.reset()
        state = self.session.current_state()
        reward = 0
        done, winner = self.session.is_session_end()

        self.num_steps = 0
        return state, reward, done

    def step(self, a: [int, int, int, int, int, int]) -> ([int], int, bool):
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

        self.num_steps += 1
        if self.num_steps > self.max_steps:
            self.reset()
            return state, reward, True
        return state, reward, done

    def _AI(self):
        switch = False
        done = False
        reward = 0
        winner = -1
        while (not switch and not done):
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
