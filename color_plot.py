
from matplotlib import pyplot as plt

x, y = [1,2,3], [1,4,9]
# col = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
col = ["black"]
for color in col:
    plt.bar(x, y, color=color, edgecolor="black")
    plt.show()
