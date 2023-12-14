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
    # TODO: Should be possible to do this in a smarter, faster way
    if dir == NORTH:
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] != SLIDING:
                    continue

                newY = y
                for checkY in reversed(range(0, y)):
                    if lines[checkY][x] == ".":
                        newY = checkY
                    else:
                        break
                lines[y][x] = EMPTY
                lines[newY][x] = SLIDING
    elif dir == SOUTH:
        for y in reversed(range(len(lines))):
            for x in range(len(lines[0])):
                if lines[y][x] != SLIDING:
                    continue

                newY = y
                for checkY in range(y+1, len(lines)):
                    if lines[checkY][x] == ".":
                        newY = checkY
                    else:
                        break
                lines[y][x] = EMPTY
                lines[newY][x] = SLIDING
    elif dir == WEST:
        for x in range(len(lines[0])):
            for y in range(len(lines)):
                if lines[y][x] != SLIDING:
                    continue

                newX = x
                for checkX in reversed(range(0, x)):
                    if lines[y][checkX] == ".":
                        newX = checkX
                    else:
                        break
                lines[y][x] = EMPTY
                lines[y][newX] = SLIDING
    elif dir == EAST:
        for x in reversed(range(len(lines[0]))):
            for y in range(len(lines)):
                if lines[y][x] != SLIDING:
                    continue

                newX = x
                for checkX in range(x+1, len(lines[0])):
                    if lines[y][checkX] == ".":
                        newX = checkX
                    else:
                        break
                lines[y][x] = EMPTY
                lines[y][newX] = SLIDING
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
    for i in range(1_000_000_000):
        cycle(lines)
        h = hashArr(lines)
        if h in seenAt:
            for _ in range((1_000_000_000 - i) % (i - seenAt[h])):
                cycle(lines)
            return load(lines)
        seenAt[h] = i


lines = read_input(14)
print(part1(lines))
print(part2(lines))