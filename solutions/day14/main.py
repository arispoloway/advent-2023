import functools
from solutions.util import read_input

EMPTY = "."
FIXED = "#"
SLIDING = "O"

NORTH = 0
WEST = 1
EAST = 2
SOUTH = 3

def parse(lines):
    return [[c for c in line] for line in lines]

def roll(lines, dir=NORTH):
    if dir == NORTH:
        for x in range(len(lines[0])):
            stones = 0
            for y in reversed(range(len(lines))):
                if lines[y][x] == SLIDING:
                    stones += 1
                elif lines[y][x] == FIXED:
                    stones = 0
                elif stones > 0:
                    lines[y][x] = SLIDING
                    lines[y+stones][x] = EMPTY
    elif dir == SOUTH:
        for x in range(len(lines[0])):
            stones = 0
            for y in range(len(lines)):
                if lines[y][x] == SLIDING:
                    stones += 1
                elif lines[y][x] == FIXED:
                    stones = 0
                elif stones > 0:
                    lines[y][x] = SLIDING
                    lines[y-stones][x] = EMPTY
    elif dir == WEST:
        for y in range(len(lines)):
            stones = 0
            for x in reversed(range(len(lines[0]))):
                if lines[y][x] == SLIDING:
                    stones += 1
                elif lines[y][x] == FIXED:
                    stones = 0
                elif stones > 0:
                    lines[y][x] = SLIDING
                    lines[y][x+stones] = EMPTY
    elif dir == EAST:
        for y in range(len(lines)):
            stones = 0
            for x in range(len(lines[0])):
                if lines[y][x] == SLIDING:
                    stones += 1
                elif lines[y][x] == FIXED:
                    stones = 0
                elif stones > 0:
                    lines[y][x] = SLIDING
                    lines[y][x-stones] = EMPTY
def cycle(lines):
    roll(lines, NORTH)
    roll(lines, WEST)
    roll(lines, SOUTH)
    roll(lines, EAST)

def load(lines):
    s = 0
    for idx, line in enumerate(lines):
        lineScore = len(lines) - idx
        for c in line:
            if c == SLIDING:
                s += lineScore
    return s

def part1(lines):
    lines = parse(lines)
    roll(lines)
    return load(lines)

def hashArr(lines):
    return hash(str(lines))

def part2(lines):
    lines = parse(lines)
    seenAt = {}
    for i in range(1, 1_000_000_000):
        cycle(lines)
        h = hashArr(lines)
        if h in seenAt:
            cycleLen = i - seenAt[h]
            while (1_000_000_000 - i) % cycleLen != 0:
                i += 1
                cycle(lines)
            return load(lines)
        seenAt[h] = i


lines = read_input(14)
print(part1(lines))
print(part2(lines))