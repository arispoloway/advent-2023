from solutions.util import read_input, withinGrid

NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

DIRS = [NORTH, SOUTH, EAST, WEST]


class Graph(object):
    def __init__(self, lines, replicas = 1):
        self.grid = []
        for _ in range(replicas):
            for line in lines:
                self.grid.append(line * replicas)
        s = int(len(lines) * replicas / 2)
        self.start = (s, s)


    # Yield node, weight
    def neighbors(self, pos):
        for dir in DIRS:
            newPos = move(pos, dir)
            if withinGrid(newPos, self.grid) and self.grid[newPos[1]][newPos[0]] != "#":
                yield newPos

    def propagate(self, times,start = None):
        if start is None:
            start = self.start
        s = set([start])
        for i in range(times):
            newS = set()
            for pos in s:
                newS.update(self.neighbors(pos))

            s = newS
        return len(s)


def move(pos, direction):
    x, y = pos
    dx, dy = direction
    return x + dx, y + dy
def part1(lines):
    return Graph(lines).propagate(64)

# Another annoying one with assumptions about the input
def part2(lines):
    totalSteps = 26501365
    stepsToNextFromCenter = int(len(lines) / 2) + 1
    l = len(lines)

    g = Graph(lines)
    fullOdd = g.propagate(135)
    fullEven = g.propagate(134)
    finalRight = g.propagate((totalSteps - stepsToNextFromCenter) % l, (0, int((l - 1) / 2)))
    finalLeft = g.propagate((totalSteps - stepsToNextFromCenter) % l, (l - 1, int((l - 1) / 2)))
    finalTop = g.propagate((totalSteps - stepsToNextFromCenter) % l, (int((l - 1) / 2), 0))
    finalBottom = g.propagate((totalSteps - stepsToNextFromCenter) % l, (int((l - 1) / 2), l - 1))

    bottomRight = g.propagate((totalSteps - stepsToNextFromCenter*2) % l, (l - 1, l - 1))
    bottomLeft = g.propagate((totalSteps - stepsToNextFromCenter*2) % l, (0, l - 1))
    topRight = g.propagate((totalSteps - stepsToNextFromCenter*2) % l, (l - 1, 0))
    topLeft = g.propagate((totalSteps - stepsToNextFromCenter*2) % l, (0, 0))

    bottomRight2 = g.propagate((totalSteps - stepsToNextFromCenter*2) % l + l, (l - 1, l - 1))
    bottomLeft2 = g.propagate((totalSteps - stepsToNextFromCenter*2) % l + l, (0, l - 1))
    topRight2 = g.propagate((totalSteps - stepsToNextFromCenter*2) % l + l, (l - 1, 0))
    topLeft2 = g.propagate((totalSteps - stepsToNextFromCenter*2) % l + l, (0, 0))

    tilesAway = int((totalSteps - stepsToNextFromCenter) / l)

    oddSum = 0
    evenSum = 0
    for i in range(1, tilesAway + 1):
        if i % 2 == 0:
            evenSum += i
        else:
            oddSum += i

    odds = evenSum * 4 + 1
    evens = oddSum * 4

    return odds * fullOdd + evens * fullEven + \
        (tilesAway + 1) * (bottomLeft + bottomRight + topLeft + topRight) + \
        tilesAway * (bottomRight2 + bottomLeft2 + topLeft2 + topRight2) + \
        finalRight + finalLeft + finalTop + finalBottom

lines = read_input(21)
print(part1(lines))
print(part2(lines))
