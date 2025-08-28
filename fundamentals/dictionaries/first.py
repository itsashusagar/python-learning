# ==============================
# 🔥 Python Dictionary Zero to Advanced
# ==============================

# 1. Create Dictionary
student = {
    "name": "Ashu",
    "age": 22,
    "course": "Python"
}
print("1. Dictionary:", student)


# 2. Access Values
print("2. Name:", student["name"])              # Ashu
print("2. Age:", student.get("age"))            # 22
print("2. Gender:", student.get("gender", "Not Found"))


# 3. Update Dictionary
student["city"] = "Delhi"      # add
student["age"] = 23            # update
print("3. Updated:", student)


# 4. Delete Items
del student["city"]
print("4. After del:", student)

student.pop("age")
print("4. After pop:", student)

student.clear()
print("4. After clear:", student)


# 5. Loop in Dictionary
student = {"name": "Ashu", "age": 22, "course": "Python"}
print("\n5. Looping:")

print("Keys:")
for k in student.keys():
    print(k)

print("Values:")
for v in student.values():
    print(v)

print("Items:")
for k, v in student.items():
    print(k, ":", v)


# 6. Dictionary Methods
student = {"name": "Ashu", "age": 22}
print("\n6. Methods:")
print("Keys:", student.keys())
print("Values:", student.values())
print("Items:", student.items())

student.update({"city": "Delhi"})
print("After update:", student)

new_student = student.copy()
print("Copied dict:", new_student)


# 7. Nested Dictionary
students = {
    "s1": {"name": "Ashu", "age": 22},
    "s2": {"name": "Rahul", "age": 25}
}
print("\n7. Nested Dictionary:", students)
print("Access nested:", students["s1"]["name"])


# 8. Dictionary Comprehension
squares = {x: x*x for x in range(1, 6)}
print("\n8. Dictionary Comprehension:", squares)


# 9. Advanced Features
# fromkeys()
keys = ["a", "b", "c"]
new_dict = dict.fromkeys(keys, 0)
print("\n9. fromkeys:", new_dict)

# setdefault()
student = {"name": "Ashu"}
student.setdefault("age", 22)
print("9. setdefault:", student)

# Sorting dictionary by values
marks = {"math": 90, "english": 75, "science": 80}
sorted_marks = dict(sorted(marks.items(), key=lambda x: x[1], reverse=True))
print("9. Sorted dict:", sorted_marks)
