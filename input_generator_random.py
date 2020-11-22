import random

def generate(n, s_max):
    input = str(n) + "\n" + str(s_max) + "\n"
    for i in range(n - 1):
        for j in range(i + 1, n):
            happiness = round(random.uniform(0, 100), 3)
            stress = round(random.uniform(0, 40/6), 3)
            input += str(i) + " " + str(j) + " " + str(happiness) + " " + str(stress) + "\n"

    with open(str(n)+".in", 'w') as fo:
        fo.write(input)


