import numpy as np
import matplotlib.pyplot as plt

# ek simple vector
v = np.array([3, 2])

# plot banate hain
plt.figure()
plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color="red")

# axis set karte hain
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Simple Vector Example")

plt.grid()
plt.show()
