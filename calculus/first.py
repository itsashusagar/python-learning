# Python Calculus Examples - Zero Level
# Install sympy if not installed: pip install sympy

import sympy as sp

# Step 1: Define the variable
x = sp.symbols('x')

# ========================
# 1. Derivative Examples
# ========================
print("----- DERIVATIVES -----")

# Example 1: f(x) = x^2 + 3x + 2
f1 = x**2 + 3*x + 2
f1_prime = sp.diff(f1, x)
print(f"Function: {f1}")
print(f"Derivative: {f1_prime}\n")

# Example 2: f(x) = sin(x)
f2 = sp.sin(x)
f2_prime = sp.diff(f2, x)
print(f"Function: {f2}")
print(f"Derivative: {f2_prime}\n")

# Example 3: f(x) = e^x
f3 = sp.exp(x)
f3_prime = sp.diff(f3, x)
print(f"Function: {f3}")
print(f"Derivative: {f3_prime}\n")

# ========================
# 2. Indefinite Integrals
# ========================
print("----- INDEFINITE INTEGRALS -----")

# Example 1: f(x) = x^2 + 3x + 2
f1_integral = sp.integrate(f1, x)
print(f"Function: {f1}")
print(f"Indefinite Integral: {f1_integral}\n")

# Example 2: f(x) = cos(x)
f2_integral = sp.integrate(sp.cos(x), x)
print(f"Function: cos(x)")
print(f"Indefinite Integral: {f2_integral}\n")

# Example 3: f(x) = e^x
f3_integral = sp.integrate(sp.exp(x), x)
print(f"Function: e^x")
print(f"Indefinite Integral: {f3_integral}\n")

# ========================
# 3. Definite Integrals
# ========================
print("----- DEFINITE INTEGRALS -----")

# Example: f(x) = x^2 + 3x + 2 from x=0 to x=2
f1_definite = sp.integrate(f1, (x, 0, 2))
print(f"Definite Integral of {f1} from 0 to 2: {f1_definite}\n")

# Example: f(x) = sin(x) from x=0 to x=pi
f2_definite = sp.integrate(sp.sin(x), (x, 0, sp.pi))
print(f"Definite Integral of sin(x) from 0 to pi: {f2_definite}\n")

# ========================
# 4. Limits
# ========================
print("----- LIMITS -----")

# Example 1: lim x->0 (sin(x)/x)
limit1 = sp.limit(sp.sin(x)/x, x, 0)
print(f"Limit of sin(x)/x as x->0: {limit1}\n")

# Example 2: lim x->inf (1/x)
limit2 = sp.limit(1/x, x, sp.oo)
print(f"Limit of 1/x as x->∞: {limit2}\n")

# Example 3: lim x->0 ((1 + x)^(1/x))
limit3 = sp.limit((1 + x)**(1/x), x, 0)
print(f"Limit of (1+x)^(1/x) as x->0: {limit3}\n")
