# Python Operators - Zero to Advanced

print("===== 1. Arithmetic Operators =====")
a, b = 10, 3
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)
print("a // b =", a // b)
print("a % b =", a % b)
print("a ** b =", a ** b)

print("\n===== 2. Comparison Operators =====")
print("a == b:", a == b)
print("a != b:", a != b)
print("a > b:", a > b)
print("a < b:", a < b)
print("a >= b:", a >= b)
print("a <= b:", a <= b)

print("\n===== 3. Logical Operators =====")
x, y = True, False
print("x and y:", x and y)
print("x or y:", x or y)
print("not x:", not x)

print("\n===== 4. Assignment Operators =====")
x = 5
print("x =", x)
x += 3
print("x += 3 ->", x)
x -= 2
print("x -= 2 ->", x)
x *= 4
print("x *= 4 ->", x)
x /= 2
print("x /= 2 ->", x)
x //= 3
print("x //= 3 ->", x)
x %= 3
print("x %= 3 ->", x)
x **= 2
print("x **= 2 ->", x)

print("\n===== 5. Bitwise Operators =====")
a, b = 5, 3   # binary: 101 & 011
print("a & b =", a & b)
print("a | b =", a | b)
print("a ^ b =", a ^ b)
print("~a =", ~a)
print("a << 1 =", a << 1)
print("a >> 1 =", a >> 1)

print("\n===== 6. Membership Operators =====")
nums = [1, 2, 3, 4]
print("2 in nums:", 2 in nums)
print("5 not in nums:", 5 not in nums)

print("\n===== 7. Identity Operators =====")
list1 = [1, 2, 3]
list2 = list1
list3 = [1, 2, 3]
print("list1 is list2:", list1 is list2)
print("list1 is list3:", list1 is list3)
print("list1 == list3:", list1 == list3)

print("\n===== 8. Operator Precedence =====")
print("2 + 3 * 4 =", 2 + 3 * 4)
print("(2 + 3) * 4 =", (2 + 3) * 4)
print("2 ** 3 ** 2 =", 2 ** 3 ** 2)

print("\n===== 9. Operator Overloading =====")
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __add__(self, other):   # Overloading +
        return Point(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"({self.x}, {self.y})"

p1 = Point(2, 3)
p2 = Point(4, 5)
print("p1 + p2 =", p1 + p2)
