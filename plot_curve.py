from matplotlib import pyplot as plt
import pickle as p

w = p.load(open("./model/999FEH linear agent.p", 'rb'))
# x = [a[0] for a in w]
# win = [a[1][2] for a in w]
# rew = [a[1][0] for a in w]

# plt.xlabel("Iterations")
# plt.ylabel("Winning Rate")
# plt.title("Winning Rate per Iteration of Linear agent")
# plt.plot(x, win)
# plt.show()

# plt.xlabel("Iterations")
# plt.ylabel("Rewards")
# plt.title("Rewards per Iteration of Linear agent")
# plt.plot(x, rew)
# plt.show()

# ites = [a[1][1] for a in w if a[1][2] == 1.0]
# x = [a[0] for a in w if a[1][2] == 1.0]
#
# plt.xlabel("Iterations")
# plt.ylabel("Steps")
# plt.title("Steps to win per episode of Linear agent")
# plt.plot(x, ites)
# plt.show()

x = [m / 40 for m in [40, 50, 60, 70, 80, 90, 100, 110, 120, 130]]
y = [1, 1, 1, .72, .83, .83, .04, .1, .03, .0]
plt.xlabel("Enemy Unit Strength")
plt.ylabel("MLP Winning Rate")
plt.title("Fully Trained MLP Agent Winning Rate Against 0.5 Difficulty Enemy")
plt.plot(x, y)
plt.show()
