import numpy as np
import matplotlib.pyplot as plt

# do vectors banate hain
v1 = np.array([2, 1])
v2 = np.array([1, 3])

# vector addition
v3 = v1 + v2  

plt.figure()

# v1
plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color="blue", label="v1")
# v2
plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color="green", label="v2")
# v1 + v2
plt.quiver(0, 0, v3[0], v3[1], angles='xy', scale_units='xy', scale=1, color="red", label="v1 + v2")

# axis set
plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Vector Addition Example")

plt.grid()
plt.legend()
plt.show()
