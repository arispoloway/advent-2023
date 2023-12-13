import math
from solutions.util import read_input


SPACE = "."
GALAXY = "#"

def parse(lines):
    emptyXs = {}
    emptyYs = {}
    emptyXCount = 0
    emptyYCount = 0

    for y, line in enumerate(lines):
        if all(c == SPACE for c in line):
            emptyYCount += 1
        emptyYs[y] = emptyYCount


    for col in range(len(lines[0])):
        if all(c == SPACE for c in map(lambda x: x[col], lines)):
            emptyXCount += 1
        emptyXs[col] = emptyXCount

    galaxies = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == GALAXY:
                galaxies.append((x, y))

    return galaxies, emptyXs, emptyYs


def calculateExpansion(lines, expansionFactor):
    galaxies, emptyXs, emptyYs = parse(lines)

    s = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i + 1:]:
            s += abs(g1[0] - g2[0]) + expansionFactor * abs(emptyXs[g1[0]] - emptyXs[g2[0]])
            s += abs(g1[1] - g2[1]) + expansionFactor * abs(emptyYs[g1[1]] - emptyYs[g2[1]])

    return s


def part1(lines):
    return calculateExpansion(lines, 1)
def part2(lines):
    return calculateExpansion(lines, 999999)

lines = read_input(11)
print(part1(lines))
print(part2(lines))