
from deepqn import model
from deepqn import memory_replay
from simulator import Simulator

import tensorflow as tf
from collections import deque
import numpy as np

identifier = "FEH MLP agent"




def train(args=None):
    gpu_ops = tf.GPUOptions(allow_growth=True)
    config = tf.ConfigProto(gpu_options=gpu_ops, log_device_placement=False)
    sess = tf.Session(config=config)

    env = Simulator()
    for i in range(8):
        env.create_unit(i, int(i / 4))



    ns = 48
    na = 4

    dqn = model.DeepQN(state_shape=(ns+na, ), num_actions=1)
    dqn.reset_sess(sess)
    dqn.set_train(lr=0.001)

    # set mr
    mr = memory_replay.MemoryReplayer((ns + na, ), capacity=10000, enabled=True)

    score = deque([], maxlen=100)


    for epi in range(5000):
        s = env.reset()

        done = False

        rc = 0

        while not done:
            a = dqn.select_action_eps_greedy(get_eps(epi), s)
            a_ = a[0]
            s_, r, done, _ = env.step(a_)
            memory_replay.MemoryReplayer.remember(s, s_, r, a_, done)
            s = s_
            rc += r
        score.append(rc)
        # replay
        s, s_, r, a, done = mr.replay(batch_size=32)
        dqn.train(s, s_, r, a, done)

        if (epi + 1) % args.performance_plot_interval == 0:
            print('train-r-mod reward avg: ', np.mean(score))


    return


def get_eps(t):
    return max(0.03, 0.6 - np.log10(100*t + 1) * 0.995)

def main():
    train()

if __name__ == "__main__":
    main()