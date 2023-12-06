import math
from solutions.util import read_input


def beatenRecords(time, distance):
    # Back to math class!
    a = -1
    b = time
    c = -distance
    root1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    root2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return math.ceil(root2) - math.ceil(root1)

def part1(lines):
    p = 1
    for (time, distance) in zip(map(int, lines[0].split()[1:]), map(int, lines[1].split()[1:])):
        p *= beatenRecords(time, distance)
    return p

def part2(lines):
    return beatenRecords(int(lines[0].split(":")[1].replace(" ", "")), int(lines[1].split(":")[1].replace(" ", "")))

lines = read_input(6)
print(part1(lines))
print(part2(lines))