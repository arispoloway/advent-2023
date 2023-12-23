from collections import defaultdict

from solutions.util import read_input, withinGrid, move

NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)

DIRS = [NORTH, SOUTH, EAST, WEST]


# I'm willing to bet that there's some isolated subgraphs here that can have the max distance through them calculated independently.
# There's probably some smart algorithm to do that, but for now this works well enough :)
class Graph(object):
    def __init__(self, lines, respectSlopes = True):
        self.grid = lines
        self.respectSlopes = respectSlopes
        self.start = (1,0)
        self.end = (len(lines[0]) - 2, len(lines) - 1)

        nodes = set(self.nodes())
        self.connections = defaultdict(set)

        for node in nodes:
            for connection in self.directConnections(node, nodes):
                self.connections[node].add(connection)

    def nodes(self):
        n = []
        n.append(self.start)
        n.append(self.end)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if len(list(self.neighbors((x, y)))) > 2:
                    n.append((x, y))
        return n

    def neighbors(self, pos):
        c = self.grid[pos[1]][pos[0]]

        dirs = DIRS

        if self.respectSlopes:
            if c == ">":
                dirs = [EAST]
            elif c == "<":
                dirs = [WEST]
            elif c == "v":
                dirs = [SOUTH]
            elif c == "^":
                dirs = [NORTH]

        for dir in dirs:
            newPos = move(pos, dir)
            if withinGrid(newPos, self.grid) and self.grid[newPos[1]][newPos[0]] != "#":
                yield newPos

    def directConnections(self, node, nodes):
        queue = [(node, 0)]
        seen = set()
        connections = []

        while len(queue) != 0:
            n, ndist = queue.pop()
            seen.add(n)

            if n != node and n in nodes:
                connections.append((n, ndist))
            else:
                for neighbor in self.neighbors(n):
                    if neighbor not in seen:
                        queue.append((neighbor, ndist + 1))
        return connections

    def longestPath(self):
        m = 0

        seen = set()
        path = [None]
        stack = [(self.start, 0, None)]

        while len(stack) != 0:
            cur, pLen, prev = stack.pop()

            # Unwind the path / visited to wherever we were when this was initially added to the stack
            while path[-1] != prev:
                seen.remove(path[-1])
                path.pop()

            if cur == self.end:
                m = max(m, pLen)
                continue

            seen.add(cur)
            path.append(cur)
            for n, weight in self.connections[cur]:
                if n not in seen:
                    stack.append((n, pLen + weight, cur))

        return m

def part1(lines):
    g = Graph(lines, respectSlopes=True)
    return g.longestPath()

def part2(lines):
    g = Graph(lines, respectSlopes=False)
    return g.longestPath()

lines = read_input(23)
print(part1(lines))
print(part2(lines))

