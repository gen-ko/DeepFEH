import sys
import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
from feh_simulator.simulator import Simulator


class fehEnv(gym.Env):
	def __init__(self):
		self.width = 6
		self.height = 8
		# input are row, col, verbose, difficulty
		self.simulator = Simulator()
		self.viewer = None
		self.seed()

	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def step(self, action):
		action_space = simulator.get_action_space()
		assert action_space.contains(action), "%r (%s) invalid"%(action, type(action))
		s, r, d = self.simulator.step(action)
		return s, r, d

	def render(self):
		screen_width = 600
		screen_height = 400
		if self.viewer is None:
			from gym.envs.classic_control import rendering
		self.viewer = rendering.Viewer(screen_width, screen_height)

		return self.viewer.render(return_rgb_array = mode=='rgb_array')

	def reset(self):
		s, r, d = self.simulator.reset()
		return s, r, d

def main(argv):
    env = fehEnv()
    s, r, done = env.reset()
    env.render()
    # while not done:
    #     action = simu.get_action_space()
    #     a = None
    #     for a_ in action:
    #         if a_.des_unit is not None:
    #             a = a_
    #             break
    #     if a is None:
    #         a = random.choice(action)
    #     s, r, done = simu.step(a)
    #     # print_info(s, r, done)
    # print_info(s, r, done)
    # s, r, done = simu.reset()
    # while not done:
    #     action = simu.get_action_space()
    #     a = None
    #     for a_ in action:
    #         if a_.des_unit is not None:
    #             a = a_
    #             break
    #     if a is None:
    #         a = random.choice(action)
    #     s, r, done = simu.step(a)
    #     # print_info(s, r, done)
    # print_info(s, r, done)

if __name__ == "__main__":
    main(sys.argv)

