from collections import defaultdict

from solutions.util import read_input

def adjacents(x, y, lines):
    ymax = len(lines)
    xmax = len(lines[0])

    coords = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y + 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
    return map(lambda c: (lines[c[1]][c[0]], c), filter(lambda c: 0 <= c[0] < xmax and 0 <= c[1] < ymax, coords))

def part1(lines):
    s = 0
    for y, line in enumerate(lines):
        curNum = ""
        adjacentSpecial = False
        for x, c in enumerate(line):
            if c in "0123456789":
                curNum = curNum + c
                for val in adjacents(x, y, lines):
                    if val[0] not in ".0123456789":
                        adjacentSpecial = True
            elif curNum != "":
                if adjacentSpecial:
                    s += int(curNum)
                curNum = ""
                adjacentSpecial = False
            else:
                adjacentSpecial = False
        if curNum != "" and adjacentSpecial:
            s += int(curNum)
    return s

def part2(lines):
    gears = defaultdict(lambda: 1)
    gearCounts = defaultdict(lambda: 0)
    s = 0
    for y, line in enumerate(lines):
        curNum = ""
        adjacentGears = set()
        for x, c in enumerate(line):
            if c in "0123456789":
                curNum = curNum + c
                for val in adjacents(x, y, lines):
                    if val[0] == "*":
                        adjacentGears.add(val[1])
            elif curNum != "":
                for gearCoord in adjacentGears:
                    gearCounts[gearCoord] += 1
                    gears[gearCoord] *= int(curNum)
                curNum = ""
                adjacentGears = set()
            else:
                adjacentGears = set()
        if curNum != "":
            for gearCoord in adjacentGears:
                gearCounts[gearCoord] += 1
                gears[gearCoord] *= int(curNum)
    for coord, gearCount in gearCounts.items():
        if gearCount == 2:
            print(coord)
            print(gears[coord])
            s += gears[coord]

    return s


lines = read_input(3)
print("day03")
print(part1(lines))
print(part2(lines))
