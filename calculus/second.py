# Advanced Python Calculus with Graphs

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Define the variable
x = sp.symbols('x')

# ========================
# 1. Function Definition
# ========================
f = sp.sin(x) * sp.exp(-0.1*x)  # Advanced function

# ========================
# 2. Derivative
# ========================
f_prime = sp.diff(f, x)

# ========================
# 3. Indefinite Integral
# ========================
f_integral = sp.integrate(f, x)

# ========================
# 4. Definite Integral
# ========================
f_definite = sp.integrate(f, (x, 0, 10))

# ========================
# 5. Limits
# ========================
limit_0 = sp.limit(f, x, 0)
limit_inf = sp.limit(f, x, sp.oo)

# ========================
# 6. Print Results
# ========================
print("Function:", f)
print("Derivative:", f_prime)
print("Indefinite Integral:", f_integral)
print("Definite Integral from 0 to 10:", f_definite)
print("Limit as x->0:", limit_0)
print("Limit as x->∞:", limit_inf)

# ========================
# 7. Graphical Visualization
# ========================

# Convert SymPy functions to numerical functions
f_num = sp.lambdify(x, f, "numpy")
f_prime_num = sp.lambdify(x, f_prime, "numpy")
f_integral_num = sp.lambdify(x, f_integral, "numpy")

# Create x values
x_vals = np.linspace(0, 20, 400)

# Plot function, derivative, and integral
plt.figure(figsize=(12, 6))
plt.plot(x_vals, f_num(x_vals), label='f(x) = sin(x) * exp(-0.1x)', color='blue')
plt.plot(x_vals, f_prime_num(x_vals), label="f'(x) (Derivative)", color='red')
plt.plot(x_vals, f_integral_num(x_vals), label="∫f(x)dx (Integral)", color='green')
plt.title("Advanced Calculus Visualization")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
