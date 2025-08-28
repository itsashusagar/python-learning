import random

trials = 1000
heads = 0

for _ in range(trials):
    if random.choice(["H", "T"]) == "H":
        heads += 1

print("Probability of Heads:", heads/trials)

trials = 10000
count = 0

for _ in range(trials):
    roll = random.randint(1, 6)
    if roll == 6:
        count += 1

print("Probability of rolling a 6:", count/trials)
