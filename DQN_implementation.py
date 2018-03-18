#!/usr/bin/env python
from random import random, randint, sample, choice

import gym
import numpy as np
from keras import Sequential, Model, Input
from keras.layers import Dense, merge
from keras.optimizers import Adam
from pickle import dump
from keras import backend as K
from simulator import Simulator


class QNetwork:

    def __init__(self, ns, na, model_name, learning_rate):
        self.model = Sequential([
                    Dense(30, input_shape=(ns + na,), activation='relu'),
                    Dense(30, input_shape=(30,), activation='relu'),
                    Dense(30, input_shape=(30,), activation='relu'),
                    Dense(30, input_shape=(30,), activation='relu'),
                    Dense(1, input_shape=(30,))
        ])
        self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))
        # # linear model
        # if model_name == "linear":
        #     print("Using linear model")
        #     self.model = Sequential([
        #         Dense(na, input_shape=(ns,))
        #     ])
        #     self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))
        #
        # # MLP
        # if model_name == "MLP":
        #     print("Using MLP model")
        #     self.model = Sequential([
        #         Dense(30, input_shape=(ns,), activation='relu'),
        #         Dense(30, input_shape=(30,), activation='relu'),
        #         Dense(30, input_shape=(30,), activation='relu'),
        #         Dense(30, input_shape=(30,), activation='relu'),
        #         Dense(na, input_shape=(30,))
        #     ])
        #     self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))
        #
        # # Duel DQN
        # if model_name == "Duel DQN":
        #     print("Using dual DQN model")
        #     input = Input(shape=(ns,))
        #     x = Dense(30, activation='relu')(input)
        #     x = Dense(30, activation='relu')(x)
        #     val_fc = Dense(30)(x)
        #     val = Dense(1)(val_fc)
        #     advantage_fc = Dense(30)(x)
        #     advantage = Dense(na)(advantage_fc)
        #     predictions = merge([val, advantage], mode=lambda y: y[0] + y[1] - K.mean(y[1]), output_shape=(na,))
        #     self.model = Model(input, predictions)
        #     self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))

    def save_model(self, name, iteration):
        # save to ./model/ directory
        self.model.save('./model/{}_{}.h5'.format(name, iteration))
        print('model saved to ./model/{}_{}.h5 on {} iteration'.format(name, iteration, iteration))

    def train(self, x_train, y_train, batch_size):
        self.model.fit(x_train, y_train, batch_size=batch_size, verbose=0)

    def qvalue(self, s):
        return self.model.predict(s)


class Memory:
    def __init__(self, memory_size=50000, burn_in=10000):
        """
        Memory unit: sa_pair, reward, next_sa_pairs, done
        """
        self.memory = []
        self.length = 0
        self.memory_size = memory_size
        self.burn_in = burn_in
        self.full = False
        # burn in
        simu = Simulator()
        for i in range(8):
            simu.create_unit(i, int(i / 4))

        iteration = 0
        while iteration <= burn_in:
            s, _, _ = simu.reset()
            while True:
                a = choice(simu.get_action_space())
                s_, r, done = simu.step(a)

                sa_pair = np.concatenate((s.flatten(), a.get_values()))
                next_sa_pairs = [np.concatenate((s_.flatten(), action.get_values())) for action in simu.get_action_space()]

                self.remember((sa_pair, r, next_sa_pairs, done))
                s = s_
                iteration += 1
                if done:
                    break
        print("Memory burned in with current index at {}".format(self.length))
        print("Memory size is {}".format(self.memory_size))

    def remember(self, transition):
        if self.full:
            self.memory[self.length] = transition
        else:
            self.memory.append(transition)
        self.length = (self.length + 1) % self.memory_size
        if self.length == 0:
            self.full = True

    def sample(self, batch_size=32):
        return sample(self.memory, batch_size)


class DQN_Agent:

    def __init__(self, identifier, model_name, learning_rate, use_replay_memory, memory_size, burn_in):
        self.simu = Simulator()
        for i in range(8):
            self.simu.create_unit(i, int(i / 4))

        self.identifier = identifier
        self.ns = 48
        self.na = 4
        self.net = QNetwork(self.ns, self.na, model_name, learning_rate)
        if use_replay_memory:
            self.memory = Memory(memory_size, burn_in)
        self.use_replay = use_replay_memory

    @staticmethod
    def epsilon_greedy_policy(q_values, eps, actions):
        if random() <= eps:
            return choice(actions)
        else:
            return actions[np.argmax(q_values)]

    def train(self, max_iteration, eps, eps_decay, eps_min, interval_iteration, gamma, test_size):
        iteration = 0
        performance = []
        while iteration <= max_iteration:
            while iteration <= max_iteration:
                s, _, _ = self.simu.reset()
                if not self.use_replay:
                    mini_batch = []
                while True:
                    eps = max(eps - eps_decay * iteration, eps_min)
                    actions = self.simu.get_action_space()
                    action_numbers = [action.get_values() for action in actions]
                    q_values = [self.net.qvalue(np.concatenate((s.flatten(), number)).reshape(1, -1))[0][0] for number in action_numbers]
                    a = self.epsilon_greedy_policy(q_values, eps, actions)

                    sa_pair = np.concatenate((s.flatten(), a.get_values()))
                    s_, r, done = self.simu.step(a)

                    next_sa_pairs = [np.concatenate((s.flatten(), action.get_values())) for action in self.simu.get_action_space()]
                    if not self.use_replay:
                        mini_batch.append((sa_pair, r, next_sa_pairs, done))
                    else:
                        mini_batch = self.memory.sample()
                        self.memory.remember((sa_pair, r, next_sa_pairs, done))

                        x_train = np.zeros((len(mini_batch), self.na + self.ns))
                        y_train = np.zeros((len(mini_batch), 1))
                        for i1, (sa_pair1, r1, next_sa_pairs1, done1) in enumerate(mini_batch):
                            # target
                            if done1 is True:
                                target = r1
                            else:
                                target = r1 + gamma * np.max([self.net.qvalue(sa_pair_) for sa_pair_ in next_sa_pairs1])
                            x_train[i1] = sa_pair1
                            y_train[i1] = target
                        self.net.train(x_train, y_train, len(mini_batch))

                        # p = self.net.qvalue()
                        #
                        # p = self.net.qvalues(np.array([i[0] for i in mini_batch]))
                        # p_ = self.net.qvalues(
                        #     np.array([(i[3] if i[4] is not None else np.zeros(self.ns)) for i in mini_batch]))
                        #
                        # x = np.zeros((len(mini_batch), self.ns))
                        # y = np.zeros((len(mini_batch), self.na))
                        #
                        # for i, val in enumerate(mini_batch):
                        #     s1 = val[0]
                        #     a1 = val[1]
                        #     r1 = val[2]
                        #     done1 = val[4]
                        #
                        #     if done1:
                        #         p[i][a1] = r1
                        #     else:
                        #         p[i][a1] = r1 + gamma * np.max(p_[i])
                        #
                        #     x[i] = s1
                        #     y[i] = p[i]
                        # self.net.train(x, y, len(mini_batch))

                    s = s_
                    iteration += 1
                    # test
                    if iteration % interval_iteration == 0:
                        performance.append((iteration, self.test(iteration, test_size=test_size)))
                        break
                    # save model
                    if iteration % int(max_iteration / 3) == 0:
                        self.net.save_model(self.identifier, iteration)
                        break
                    if done:
                        # print("hold for {} sec".format(i - start))
                        break

                # if not self.use_replay:
                #     x_train = np.zeros((len(mini_batch), self.ns))
                #     y_train = np.zeros((len(mini_batch), self.na))
                #     for i1, (s1, a1, r1, s_1, done) in enumerate(mini_batch):
                #         q_values1 = self.net.qvalues(np.array([s1]))[0]
                #         if done:
                #             q_values1[a1] = r1
                #         else:
                #             q_values1[a1] = r1 + gamma * np.max(self.net.qvalues(np.array([s_1])))
                #         x_train[i1] = s1
                #         y_train[i1] = q_values1
                #     self.net.train(x_train, y_train, len(mini_batch))
        dump(performance, open('./model/{}.p'.format(self.identifier), 'wb'))

    def test(self, iteration, test_size):
        rewards = 0
        for _ in range(test_size):
            s2, _, _ = self.simu.reset()
            while True:
                actions = self.simu.get_action_space()
                q_values = [self.net.qvalue(np.concatenate((s2.flatten(), action))) for action in actions]
                a = self.epsilon_greedy_policy(q_values, 0, actions)
                s2, r2, done2 = self.simu.step(a)
                rewards += r2
                if done2:
                    break
        print("The average reward of {} iteration is {}".format(iteration, rewards / test_size))
        return rewards / test_size


def main(identifier, model_name, max_iteration, epsilon, epsilon_decay, epsilon_min, interval_iteration, gamma,
         test_size, learning_rate, use_replay_memory, memory_size, burn_in):
    agent = DQN_Agent(identifier=identifier, model_name=model_name, learning_rate=learning_rate,
                      use_replay_memory=use_replay_memory, memory_size=memory_size, burn_in=burn_in)
    agent.train(max_iteration=max_iteration, eps=epsilon, eps_decay=epsilon_decay,
                eps_min=epsilon_min, interval_iteration=interval_iteration, gamma=gamma, test_size=test_size)
