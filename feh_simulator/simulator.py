from feh_simulator.session import Session

"""
Simple assumption:
    Team0 is always friendly and Team1 is enemy.
    Team0 will always be offensive
    Enemy has random strategy
    Enemy will act from first role to last role in sequence
"""

class Simulator:
    def __init__(self, verbose=True, difficulty=1.0, team):
        self.verbose = verbose
        self.difficulty = difficulty
        self.session = None
        self.myTeam = team

    def create_unit(self,map_file='./map_data/map_01.txt',
                    unit_files=['./unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',
                           './unit_data/unit_default.txt',],
                    unit_teams=[1, 1, 1, 1, 2, 2, 2, 2]):
        """
        customize unit as you want
        """
        sess = Session(map_file, unit_files, unit_teams)

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
        return state, reward, done

    def step(self, a:[int, int, int, int, int, int]) -> ([int], int, bool):
        """
        Reset the FEH environment, returning current locations, reward and done.
        """
        self.session.operate(a)
        state = self.session.current_state()
        reward = 0
        done, winner = self.session.is_session_end()
        if winner == self.team:
            reward = 100
            return state, reward, done
        else:
            reward = -100
            return state, reward, done
        actions = self.get_action_space()
        if len(actions) == 0:
            state, reward, done = self._AI()
        return state, reward, done

    def _AI(self):



def main(argv):
    simu = Simulator()
    simu.create_unit(team=0, x=0, y=0)
    simu.create_unit(team=1, x=4, y=4)
    s, r, done = simu.reset()
    print_info(simu, r, done)
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