from matplotlib import pyplot as plt
import pickle as p

w = p.load(open("./model/198FEH MLP agent.p", 'rb'))
x = [a[0] for a in w]
win = [a[1][2] for a in w]

rew = [a[1][0] for a in w]

plt.xlabel("Iterations")
plt.ylabel("Winning Rate")
plt.title("Winning Rate per Iteration of MLP agent")
plt.plot(x, win)
plt.show()

# plt.xlabel("Iterations")
# plt.ylabel("Rewards")
# plt.title("Rewards per Iteration of MLP agent")
# plt.plot(x, rew)
# plt.show()

# ites = [a[1][1] for a in w if a[1][2] == 1.0]
# x = [a[0] for a in w if a[1][2] == 1.0]
#
# plt.xlabel("Iterations")
# plt.ylabel("Steps")
# plt.title("Steps to win per episode of MLP agent")
# plt.plot(x, ites)
# plt.show()
