import sys

import numpy as np
import gym
import pickle
import matplotlib
import sys

from model import PolicyNet

MIN_PYTHON = (3, 6)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


matplotlib.use('Agg')
import matplotlib.pyplot as plt


class Reinforce(object):
    # Implementation of the policy gradient method REINFORCE.

    def __init__(self, env, lr, gamma, save_path, load=False):
        self.mean = []
        self.std = []
        self.env = env
        s_len = self.env.observation_space.shape[0]
        a_len = self.env.action_space.n
        self.model = PolicyNet(lr,  s_len, a_len)
        self.gamma = gamma
        self.save_path = save_path
        if load:
            self.model.load(self.save_path)
        return

    def train(self):
        # Trains the model on a single episode using REINFORCE.
        #       method generate_episode() to generate training data.
        K = 100
        print("pretrain test:")
        self.test()
        print("training")
        # generate an episode
        for i in range(10000000):
            s, a, r = self.generate_episode()
            s = np.array(s)
            r = np.array(r)
            r /= 100.0
            T = len(r)
            G = np.zeros(shape=(T,), dtype=np.float32)
            G[T - 1] = r[T - 1]
            for t in range(T - 2, -1, -1):
                G[t] = self.gamma * G[t+1] + r[t]
            for j in range(6):
                self.model.fit(s, a, G)
            if (i + 1) % K == 0:
                mean, std = self.test()
                self.mean.append(mean)
                self.std.append(std)
                with open('mean_np_array.pickle', 'wb+') as f:
                    pickle.dump(self.mean, f)
                with open('std_np_array.pickle', 'wb+') as f:
                    pickle.dump(self.std, f)
                self.model.save(self.save_path)
        self.model.save(self.save_path)
        return

    def generate_episode_fast(self):
        s = self.env.reset()
        done = False
        states = []
        rewards = []
        predict_fn = self.model.predict
        step_fn = self.env.step
        s_append_fn = states.append
        r_append_fn = rewards.append
        while not done:
            a = predict_fn(s.reshape([1, -1]))
            s_append_fn(s)
            s, r, done, _ = step_fn(a)
            r_append_fn(r)
        return states, rewards

    def generate_episode(self):
        s = self.env.reset()
        done = False
        states = []
        rewards = []
        actions = []
        predict_fn = self.model.predict
        step_fn = self.env.step
        s_append_fn = states.append
        r_append_fn = rewards.append
        a_append_fn = actions.append
        while not done:
            a = predict_fn(s.reshape([1, -1]))
            a_append_fn(a)
            s_append_fn(s)
            s, r, done, _ = step_fn(a)
            r_append_fn(r)
        return states, actions, rewards
    
    def generate_episode_render(self):
        s = self.env.reset()
        done = False
        states = []
        rewards = []
        predict_fn = self.model.predict
        step_fn = self.env.step
        s_append_fn = states.append
        r_append_fn = rewards.append
        while not done:
            self.env.render()
            a = predict_fn(s.reshape([1, -1]))
            s_append_fn(s)
            s, r, done, _ = step_fn(a)
            r_append_fn(r)
        self.env.render()
        return states, rewards

    def test(self):
        r = []
        for i in range(100):
            _, ri = self.generate_episode_fast()
            ri = sum(ri)
            r.append(ri)

        std = np.std(r)
        mean = np.mean(r)
        print('r =', mean, "+-", std)
        return mean, std
    
    def test_render(self):
        r = []
        for i in range(100):
            _, ri = self.generate_episode_render()
            ri = sum(ri)
            r.append(ri)
        steps = len(r)
        std = np.std(r)
        mean = np.mean(r)
        print('r =', mean, "+-", std, "steps", steps)
        return mean, std


def main():
    env = gym.make('LunarLander-v2')

    rf = Reinforce(env=env, lr=0.0001, gamma=0.99, save_path="./reinforce_luna-v2.h5", load=True)
    rf.train()
    return


if __name__ == '__main__':
    if __debug__:
        print("debug mode ON")
    else:
        print("debug mode OFF")
    main()
