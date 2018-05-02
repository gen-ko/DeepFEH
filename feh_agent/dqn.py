#!/usr/bin/env python
from pickle import dump
from random import random, sample, choice

import numpy as np
from keras import Sequential, Model
from keras.layers import Dense, Input, Lambda, add, concatenate
from keras.optimizers import Adam
from keras import backend as K

from feh_simulator.simulator import Simulator


class QNetwork:

    def __init__(self, ns, na, model_name, learning_rate):
        self.model = None
        # linear model
        if model_name == "linear":
            print("Using linear model")
            self.model = Sequential([
                Dense(1, input_shape=(ns + na,))
            ])
            self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))

        # MLP
        if model_name == "MLP":
            print("Using MLP model")
            self.model = Sequential([
                Dense(50, input_shape=(ns + na,), activation='relu'),
                Dense(50, input_shape=(50,), activation='relu'),
                Dense(50, input_shape=(50,), activation='relu'),
                Dense(50, input_shape=(50,), activation='relu'),
                Dense(1, input_shape=(50,))
            ])
            self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))

        # Duel DQN
        if model_name == "Duel DQN":
            print("Using duel DQN model")
            input = Input(shape=(ns + na,))
            states = Lambda(lambda x: x[:, :ns], output_shape=(ns,))(input)
            # state value V(s)
            x = Dense(30)(states)
            x = Dense(30)(x)
            x = Dense(30)(x)
            x = Dense(30)(x)
            value = Dense(1)(x)
            # action advantage A(s, a)
            y = Dense(30)(input)
            y = Dense(30)(y)
            y = Dense(30)(y)
            y = Dense(30)(y)
            advantage = Dense(1)(y)
            # Q(s, a) = V(s) + A(s, a)
            output = add([value, advantage])
            self.model = Model(input, output)
            self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate))

    def save_model(self, name, iteration):
        # save to ./model/ directory
        self.model.save('./model/{}_{}.h5'.format(name, iteration))
        print('model saved to ./model/{}_{}.h5 on {} iteration'.format(name, iteration, iteration))

    def train(self, x_train, y_train, batch_size):
        self.model.fit(x_train, y_train, batch_size=batch_size, verbose=0)

    def qvalue(self, s):
        return self.model.predict(s)


class Memory:
    def __init__(self, simu, memory_size=50000, burn_in=10000, difficulty=0.0):
        """
        Memory unit: sa_pair, reward, next_sa_pairs, done
        """
        self.memory = []
        self.length = 0
        self.memory_size = memory_size
        self.burn_in = burn_in
        self.full = False
        # burn in
        iteration = 0
        while iteration <= burn_in:
            s, _, _ = simu.reset()
            while True:
                a = choice(simu.get_action_space())
                s_, r, done = simu.step(a)

                sa_pair = np.concatenate((np.array(s).flatten(), np.array(a)))
                next_sa_pairs = [np.concatenate((np.array(s_).flatten(), np.array(action))) for action in
                                 simu.get_action_space()]

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

    def __init__(self, identifier, ns, na, model_name, learning_rate, use_replay_memory, memory_size, burn_in, difficulty):
        self.difficulty = difficulty
        self.simu = Simulator(verbose=False, difficulty=difficulty)
        self.simu.create_unit()
        self.identifier = identifier
        self.ns = ns
        self.na = na
        self.net = QNetwork(self.ns, self.na, model_name, learning_rate)
        if use_replay_memory:
            self.memory = Memory(self.simu, memory_size, burn_in, difficulty)
        self.use_replay = use_replay_memory

    @staticmethod
    def epsilon_greedy_policy(q_values, eps, actions):
        if random() <= eps:
            return choice(actions)
        else:
            return actions[np.argmax(q_values)]

    def train(self, max_iteration, eps, eps_decay, eps_min, interval_iteration, gamma, test_size):
        self.test(0, test_size=test_size)
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
                    action_numbers = [np.array(action) for action in actions]
                    q_values = [self.net.qvalue(np.concatenate((np.array(s).flatten(), np.array(number))).reshape(1, -1))[0][0] for number
                                in action_numbers]
                    a = self.epsilon_greedy_policy(q_values, eps, actions)

                    sa_pair = np.concatenate((np.array(s).flatten(), np.array(a)))
                    s_, r, done = self.simu.step(a)

                    next_sa_pairs = [np.concatenate((np.array(s).flatten(), np.array(action))) for action in
                                     self.simu.get_action_space()]
                    if not self.use_replay:
                        mini_batch.append((sa_pair, r, next_sa_pairs, done))
                    else:
                        mini_batch = self.memory.sample()
                        self.memory.remember((sa_pair, r, next_sa_pairs, done))
                        self.train_on_minibatch(mini_batch, gamma)

                    s = s_
                    iteration += 1
                    # save model
                    if iteration % int(max_iteration / 3) == 0:
                        self.net.save_model(self.identifier, iteration)
                        dump(performance, open('./model/{}{}.p'.format(iteration, self.identifier), 'wb'))
                        break
                    # test
                    if iteration % interval_iteration == 0:
                        performance.append((iteration, self.test(iteration, test_size=test_size)))
                        break
                    if done:
                        # print("hold for {} sec".format(i - start))
                        break

                if not self.use_replay:
                    self.train_on_minibatch(mini_batch, gamma)

        dump(performance, open('./model/{}.p'.format(self.identifier), 'wb'))

    def test(self, iteration, test_size):
        rewards = 0
        count = 0
        win_round = 0
        for _ in range(test_size):
            s2, _, _ = self.simu.reset()
            while True:
                actions = self.simu.get_action_space()
                q_values = [self.net.qvalue(np.concatenate((np.array(s2).flatten(), np.array(action))).reshape(1, -1))[0][0]
                            for action in actions]
                a = self.epsilon_greedy_policy(q_values, 0, actions)
                s2, r2, done2 = self.simu.step(a)
                rewards += r2
                count += 1
                if done2:
                    if r2 == 100:
                        win_round += 1
                    break
        print("The average reward of {} iteration is {}".format(iteration, rewards / test_size))
        print("The average iterations taken per episode is {}".format(count / test_size))
        print("The win rate of this model is {}".format(win_round / test_size))
        return rewards / test_size, count / test_size, win_round / test_size

    def train_on_minibatch(self, mini_batch, gamma):
        x_train = np.zeros((len(mini_batch), self.na + self.ns))
        y_train = np.zeros((len(mini_batch), 1))
        for i1, (sa_pair1, r1, next_sa_pairs1, done1) in enumerate(mini_batch):
            # target
            if done1 is True:
                target = r1
            else:
                target = r1 + gamma * np.max(
                    [self.net.qvalue(sa_pair_.reshape(1, -1))[0][0] for sa_pair_ in next_sa_pairs1])
            x_train[i1] = sa_pair1
            y_train[i1] = target
        self.net.train(x_train, y_train, len(mini_batch))


def main(identifier, ns, na, model_name, max_iteration, epsilon, epsilon_decay, epsilon_min, interval_iteration, gamma,
         test_size, learning_rate, use_replay_memory, memory_size, burn_in, difficulty):
    agent = DQN_Agent(identifier=identifier, ns=ns, na=na, model_name=model_name, learning_rate=learning_rate,
                      use_replay_memory=use_replay_memory, memory_size=memory_size, burn_in=burn_in,
                      difficulty=difficulty)
    agent.train(max_iteration=max_iteration, eps=epsilon, eps_decay=epsilon_decay,
                eps_min=epsilon_min, interval_iteration=interval_iteration, gamma=gamma, test_size=test_size)
