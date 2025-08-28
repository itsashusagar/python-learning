# 🚀 Python Data Types Full Examples (Zero to Advanced)

# 1. Numbers
a = 10        # int
b = 3.14      # float
c = 2 + 3j    # complex
print("Numbers:", a, b, c)

# 2. String
name = "Ashu"
greet = 'Hello'
sentence = """This is
a multi-line string"""
print("String Examples:", name, greet, sentence)
print("Upper:", name.upper())
print("Length of greet:", len(greet))

# 3. Boolean
is_active = True
is_logged_in = False
print("Booleans:", is_active, is_logged_in)
print("5 > 3 ?", 5 > 3)

# 4. List
fruits = ["apple", "banana", "mango"]
print("Fruits List:", fruits)
print("First fruit:", fruits[0])
fruits.append("grape")
print("After append:", fruits)

# 5. Tuple
colors = ("red", "blue", "green")
print("Tuple:", colors)
print("Second color:", colors[1])

# 6. Set
nums = {1, 2, 3, 3, 2}
print("Set:", nums)   # duplicates removed

# 7. Dictionary
student = {
    "name": "Ashu",
    "age": 21,
    "marks": 90
}
print("Dictionary:", student)
print("Student Name:", student["name"])
student["age"] = 22
print("Updated Dictionary:", student)

# 8. NoneType
x = None
print("NoneType Example:", x)

# 9. Bytes
b = bytes([65, 66, 67])
print("Bytes:", b)

# 10. Bytearray
ba = bytearray([65, 66, 67])
ba[0] = 90
print("Bytearray:", ba)

# 11. Range
r = range(5)
print("Range:", list(r))

# 12. Frozenset
fs = frozenset([1, 2, 3, 3])
print("Frozenset:", fs)

# 13. Type Casting (Type Conversion)
num = 10
f = float(num)   # int -> float
s = str(num)     # int -> string
print("Casting Examples:", f, s, type(f), type(s))
