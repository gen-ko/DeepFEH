import numpy as np
from keras.models import load_model

from simulator import Simulator

name = "FEH MLP agent_333.h5"
test_size = 20

model = load_model('./model/{}'.format(name))

simu = Simulator(verbose=False)
for i in range(8):
    simu.create_unit(i, int(i / 4))
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
print("The average reward of model {} iteration is {}".format(name, rewards / test_size))
print("The average iterations taken per episode is {}".format(count / test_size))
print("The win rate of this model is {}".format(win_round / test_size))
