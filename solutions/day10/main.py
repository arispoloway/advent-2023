import math
from solutions.util import read_input


def withinGrid(pos, grid):
    return 0 <= pos[0] < len(grid[0]) and 0 <= pos[1] < len(grid)

def parse(lines):
    start = None
    graph = {}

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            connectedTo = []
            if char == ".":
                continue
            elif char == "|":
                connectedTo = [(x, y - 1), (x, y + 1)]
            elif char == "-":
                connectedTo = [(x - 1, y), (x + 1, y)]
            elif char == "L":
                connectedTo = [(x, y - 1), (x + 1, y)]
            elif char == "J":
                connectedTo = [(x, y - 1), (x - 1, y)]
            elif char == "7":
                connectedTo = [(x, y + 1), (x - 1, y)]
            elif char == "F":
                connectedTo = [(x, y + 1), (x + 1, y)]
            elif char == "S":
                start = (x, y)
                if lines[y + 1][x] in "7F|":
                    connectedTo.append((x, y+1))
                if lines[y - 1][x] in "JL|":
                    connectedTo.append((x, y + 1))
                if lines[y][x+1] in "-J7":
                    connectedTo.append((x, y + 1))
                if lines[y][x - 1] in "-FL":
                    connectedTo.append((x, y + 1))
            graph[(x,y)] = [link for link in connectedTo if withinGrid(link, lines)]
    return graph, start


def adjacents(x, y, lines):
    ymax = len(lines)
    xmax = len(lines[0])

    coords = [(x - 1, y), (x, y + 1), (x, y - 1),  (x + 1, y)]
    return filter(lambda c: 0 <= c[0] < xmax and 0 <= c[1] < ymax, coords)

def part1(lines):
    graph, start = parse(lines)
    steps = 1
    prevNode = start
    curNode = graph[start][0]
    while curNode != start:
        steps += 1
        nextNode = next(node for node in graph[curNode] if node != prevNode)
        prevNode, curNode = curNode, nextNode
    return int(steps / 2)


def floodFill(grid, fillWith, start):
    toFill = {start}
    amountFilled = 0
    touchesBorder = False
    while len(toFill) != 0:
        x, y = next(iter(toFill))
        toFill.remove((x, y))

        loc = grid[y][x]
        if loc != EMPTY:
            continue

        grid[y][x] = fillWith
        amountFilled += 1
        if x == 0 or y == 0 or y == (len(grid) - 1) or x == (len(grid[0]) - 1):
            touchesBorder = True
        for n in adjacents(x, y, grid):
            toFill.add(n)
    return amountFilled, touchesBorder


EMPTY = " "
BOUNDARY = "B"
FILL = "."
def part2(lines):
    graph, start = parse(lines)
    steps = 1

    grid = [[EMPTY for _ in line] for line in lines]

    prevNode = start
    grid[start[1]][start[0]] = BOUNDARY
    curNode = graph[start][0]
    rightSides = set()
    leftSides = set()
    while curNode != start:

        x, y = curNode

        grid[curNode[1]][curNode[0]] = BOUNDARY
        steps += 1
        nextNode = next(node for node in graph[curNode] if node != prevNode)

        deltaX = curNode[0] - prevNode[0]
        deltaY = curNode[1] - prevNode[1]
        deltaX2 = nextNode[0] - curNode[0]
        deltaY2 = nextNode[1] - curNode[1]

        if deltaX == 1:
            if deltaX2 == 1:
                rightSides.add((x, y + 1))
                leftSides.add((x, y - 1))
            elif deltaY2 == 1:
                leftSides.add((x + 1, y))
                leftSides.add((x, y-1))
            elif deltaY2 == -1:
                rightSides.add((x + 1, y))
                rightSides.add((x, y+1))
        if deltaX == -1:
            if deltaX2 == -1:
                leftSides.add((x, y + 1))
                rightSides.add((x, y - 1))
            elif deltaY2 == 1:
                rightSides.add((x - 1, y))
                rightSides.add((x, y-1))
            elif deltaY2 == -1:
                leftSides.add((x - 1, y))
                leftSides.add((x, y+1))
        if deltaY == 1:
            if deltaY2 == 1:
                leftSides.add((x + 1, y))
                rightSides.add((x - 1, y))
            elif deltaX2 == 1:
                rightSides.add((x - 1, y))
                rightSides.add((x, y+1))
            elif deltaX2 == -1:
                leftSides.add((x + 1, y))
                leftSides.add((x, y+1))
        if deltaY == -1:
            if deltaY2 == -1:
                leftSides.add((x - 1, y))
                rightSides.add((x + 1, y))
            elif deltaX2 == 1:
                leftSides.add((x - 1, y))
                leftSides.add((x, y-1))
            elif deltaX2 == -1:
                rightSides.add((x + 1, y))
                rightSides.add((x, y-1))

        prevNode, curNode = curNode, nextNode


    s = 0
    borderTouch = False
    for right in filter(lambda x: withinGrid(x, grid), rightSides):
        amount, border = floodFill(grid, FILL, right)
        s += amount
        borderTouch |= border
    if not borderTouch:
        return s

    s = 0
    for left in filter(lambda x: withinGrid(x, grid), leftSides):
        amount, _ = floodFill(grid, FILL, left)
        s += amount
    return s


lines = read_input(10)
print(part1(lines))
print(part2(lines))
