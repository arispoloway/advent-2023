import functools
import queue

from solutions.util import read_input, withinGrid

from collections import defaultdict, OrderedDict

NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

DIRS = [NORTH, SOUTH, EAST, WEST]

def isOpposite(dir1, dir2):
    if dir1 == NORTH:
        return dir2 == SOUTH
    if dir1 == SOUTH:
        return dir2 == NORTH
    if dir1 == EAST:
        return dir2 == WEST
    if dir1 == WEST:
        return dir2 == EAST

# Node is ((x, y), prev direction, # steps in that direction

class Graph(object):
    def __init__(self, lines, minSteps, maxSteps):
        self.grid = lines
        self.minSteps = minSteps
        self.maxSteps = maxSteps

    # Yield node, weight
    def neighbors(self, node):
        pos, prevDirection, prevSteps = node
        for dir in DIRS:
            if isOpposite(prevDirection, dir):
                continue

            if prevDirection == dir and prevSteps < self.maxSteps:
                newPos = move(pos, dir)
                if withinGrid(newPos, self.grid):
                    yield (newPos, dir, prevSteps + 1), self.grid[newPos[1]][newPos[0]]
            elif prevDirection != dir and prevSteps >= self.minSteps:
                newPos = move(pos, dir)
                if withinGrid(newPos, self.grid):
                    yield (newPos, dir, 1), self.grid[newPos[1]][newPos[0]]

    def shortestPath(self, start, end):
        q = queue.PriorityQueue()
        q.put((0, (start, EAST, 0)))
        q.put((0, (start, SOUTH, 0)))
        q.put((0, (start, NORTH, 0)))
        q.put((0, (start, WEST, 0)))

        bestPath = {}

        while not q.empty():
            score, node = q.get()
            if node[0] == end:
                return score
            if node in bestPath:
                continue
            bestPath[node] = score
            for (neighbor, weight) in self.neighbors(node):
                if neighbor in bestPath:
                    continue
                q.put((score + weight, neighbor))


def move(pos, direction):
    x, y = pos
    dx, dy = direction
    return x + dx, y + dy
def part1(lines):
    grid = [[int(c) for c in line] for line in lines]
    return Graph(grid, 0, 3).shortestPath((0, 0), (len(lines[0]) - 1, len(lines) - 1))
def part2(lines):
    grid = [[int(c) for c in line] for line in lines]
    return Graph(grid, 4, 10).shortestPath((0, 0), (len(lines[0]) - 1, len(lines) - 1))


lines = read_input(17)
print(part1(lines))
print(part2(lines))