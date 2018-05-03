import numpy as np
import gym

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reinforce import Reinforce
from model import CriticNet

import feh_simulator.simulator as gym

class A2C(Reinforce):
    # Implementation of N-step Advantage Actor Critic.
    # This class inherits the Reinforce class, so for example, you can reuse
    # generate_episode() here.

    def __init__(self, env, lr, critic_lr, gamma, n, policy_path, critic_path, load=False):
        # Initializes A2C.
        # Args:
        # - model: The actor model.
        # - lr: Learning rate for the actor model.
        # - critic_model: The critic model.
        # - critic_lr: Learning rate for the critic model.
        # - n: The value of N in N-step A2C.
        Reinforce.__init__(self, env, lr, gamma=gamma, save_path=policy_path, load=load)
        self.critic_path = critic_path
        s_len = self.env.observation_space_shape[0]
        self.critic = CriticNet(critic_lr, s_len=s_len)
        self.n = n
        if load:
            self.critic.load(self.critic_path)
        print("Hyperparameters:\nPolicy LR = {} Critic LR = {} Gamma = {} N = {} \nPolicy Path = {} \nCritic Path = {} \nLoad = {}".format(
            lr, critic_lr, gamma, n, policy_path, critic_path, load
        ))
        return

    def train(self):
        # Trains the model on a single episode using A2C.
        K = 500
        print("pretrain test:")
        print('episode 0 ', end='')
        self.test()
        print("training")
        # generate an episode
        gamma_n_1 = self.gamma ** (self.n - 1)
        gamma_n = gamma_n_1 * self.gamma
        for i in range(10000000):
            s, ava, a, r = self.generate_episode()
            s = np.array(s)
            r = np.array(r)
            r /= 100.0
            T = len(r)
            if self.n >= T:
                n = T - 1
            else:
                n = self.n
            sum_r = np.zeros(shape=(T, ), dtype=np.float32)
            sum_r[T - 1] = r[T - 1]
            for p in range(2, n + 1, 1):
                sum_r[T - p] = sum_r[T - p + 1] * self.gamma + r[T - p]
            for q in range(n + 1, T + 1, 1):
                sum_r[T - q] = (sum_r[T - q + 1] - gamma_n_1 * r[T - q + n]) * self.gamma + r[T - q]

            V_end = np.zeros(shape=(T,), dtype=np.float32)

            for j in range(6):
                V = self.critic.predict(s)
                V_end[0:T-n] = V[n: T]
                R = gamma_n * V_end + sum_r
                G = R - V          
                self.model.fit(s, ava, a, G)
                self.critic.fit(s, R)
                
            if (i + 1) % K == 0:
                print('episode {} '.format(i + 1), end='')
                self.test()
                self.model.save(self.save_path)
                self.critic.save(self.critic_path)
        self.model.save(self.save_path)
        return


def main():
    env = gym.make('FEH-v1')
    n = 50
    a2c = A2C(env=env, lr=0.0001,  gamma=0.99, critic_lr=0.0001, n=n,
              policy_path="./saved_model/a2c_policy-v2-n{}.h5".format(n),
              critic_path="./saved_model/a2c_critic_v2-n{}.h5".format(n),
              load=False)
    a2c.train()
    return


if __name__ == '__main__':
    main()
