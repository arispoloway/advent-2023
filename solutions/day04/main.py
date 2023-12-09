from collections import defaultdict

from solutions.util import read_input

def part1(lines):
    s = 0
    for line in lines:
        x = line.split(": ")[1].split(" | ")
        count = len(set(x[0].strip().split()).intersection(set(x[1].strip().split())))
        if count >= 1:
            s += 2 ** (count - 1)
    return s

def part2(lines):
    copies = defaultdict(lambda: 0)
    for i, line in enumerate(lines):
        copies[i] += 1
        x = line.split(": ")[1].split(" | ")
        count = len(set(x[0].strip().split()).intersection(set(x[1].strip().split())))
        for j in range(i + 1, i + 1 + count):
            copies[j] += copies[i]
    return sum(copies.values())

lines = read_input(4)
print(part1(lines))
print(part2(lines))
