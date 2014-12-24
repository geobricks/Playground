import numpy as np
import matplotlib.pyplot as plt

s = np.random.poisson(30, 300)

count, bins, ignored = plt.hist(s, 14, normed=True)
plt.show()