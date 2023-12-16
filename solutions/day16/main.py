import functools
from solutions.util import read_input, withinGrid

from collections import defaultdict, OrderedDict

# TODO: I'm sure there's some nice optimization because most of the work is duplicated

EMPTY = "."
VERTICAL = "|"
HORIZONTAL = "-"
LEFTRIGHT = "\\"
RIGHTLEFT = "/"

NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

def move(pos, direction):
    x, y = pos
    dx, dy = direction
    return x + dx, y + dy

def transformBeams(pos, direction, grid):
    x, y = pos
    if grid[y][x] == EMPTY:
        return [(pos, direction)]
    elif grid[y][x] == VERTICAL:
        if direction in [NORTH, SOUTH]:
            return [(pos, direction)]
        return [(pos, NORTH), (pos, SOUTH)]
    elif grid[y][x] == HORIZONTAL:
        if direction in [EAST, WEST]:
            return [(pos, direction)]
        return [(pos, EAST), (pos, WEST)]
    elif grid[y][x] == LEFTRIGHT:
        if direction == NORTH:
            return [(pos, WEST)]
        if direction == SOUTH:
            return [(pos, EAST)]
        if direction == EAST:
            return [(pos, SOUTH)]
        if direction == WEST:
            return [(pos, NORTH)]
    elif grid[y][x] == RIGHTLEFT:
        if direction == NORTH:
            return [(pos, EAST)]
        if direction == SOUTH:
            return [(pos, WEST)]
        if direction == EAST:
            return [(pos, NORTH)]
        if direction == WEST:
            return [(pos, SOUTH)]

    raise "BOOM"

def energizedBeams(beam, lines):
    seen = defaultdict(set)
    beams = set()

    pos, direction = beam

    for newBeam in transformBeams(pos, direction, lines):
        if withinGrid(newBeam[0], lines):
            seen[newBeam[0]].add(newBeam[1])
            beams.add(newBeam)

    while len(beams) != 0:
        n = next(iter(beams))
        beams.remove(n)
        pos, direction = n
        newPos = move(pos, direction)
        if not withinGrid(newPos, lines):
            continue
        newBeams = transformBeams(newPos, direction, lines)

        for newBeam in newBeams:
            if withinGrid(newBeam[0], lines) and newBeam[1] not in seen[newBeam[0]]:
                seen[newBeam[0]].add(newBeam[1])
                beams.add(newBeam)
    return len(seen)


def part1(lines):
    return energizedBeams(((0,0), EAST), lines)

def edgeBeams(lines):
    for y in range(len(lines)):
        yield ((0, y), EAST)
        yield ((len(lines[0]) - 1, y), WEST)
    for x in range(len(lines[0])):
        yield ((x, 0), SOUTH)
        yield ((x, len(lines) - 1), NORTH)

def part2(lines):
    return max(energizedBeams(beam, lines) for beam in edgeBeams(lines))



lines = read_input(16)
print(part1(lines))
print(part2(lines))