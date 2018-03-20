import numpy as np
from keras.models import load_model

from simulator import Simulator

name = "FEH MLP agent_198.h5"
test_size = 100

model = load_model('./model/{}'.format(name))
wins = []
for iteration in range(5):
    simu = Simulator(verbose=False)
    simu.create_unit(0, 0, 40)
    simu.create_unit(1, 0, 40)
    simu.create_unit(2, 0, 40)
    simu.create_unit(3, 0, 40)
    simu.create_unit(4, 1, 40 + 100 * iteration)
    simu.create_unit(5, 1, 40 + 100 * iteration)
    simu.create_unit(6, 1, 40 + 100 * iteration)
    simu.create_unit(7, 1, 40 + 100 * iteration)
    rewards = 0
    count = 0
    win_round = 0
    for _ in range(test_size):
        s2, _, _ = simu.reset()
        while True:
            actions = simu.get_action_space()
            q_values = [model.predict(np.concatenate((s2.flatten(), action.get_values())).reshape(1, -1))[0][0] for action
                        in actions]
            a = actions[np.argmax(q_values)]
            s2, r2, done2 = simu.step(a)
            rewards += r2
            count += 1
            if done2:
                if r2 == 100:
                    win_round += 1
                break
    print("The win rate of this model is {}".format(win_round / test_size))
    wins.append(win_round / test_size)

print(wins)
