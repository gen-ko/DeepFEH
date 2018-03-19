from matplotlib import pyplot as plt
import pickle as p

w = p.load(open("./model/198FEH linear agent.p", 'rb'))
x = [a[0] for a in w]
win = [a[1][2] for a in w]
rew = [a[1][0] for a in w]

plt.xlabel("Iterations")
plt.ylabel("Winning Rate")
plt.title("Winning Rate per Iteration of linear agent")
plt.plot(x, win)
plt.show()

plt.xlabel("Iterations")
plt.ylabel("Rewards")
plt.title("Rewards per Iteration of linear agent")
plt.plot(x, rew)
plt.show()
