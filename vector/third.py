import numpy as np
import matplotlib.pyplot as plt

# Vectors
v1 = np.array([3, 2])
v2 = np.array([1, 4])

# Plot
plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='r', label='v1')
plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='b', label='v2')

plt.xlim(0, 5)
plt.ylim(0, 5)
plt.grid()
plt.legend()
plt.show()
