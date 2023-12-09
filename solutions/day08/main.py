import math
from solutions.util import read_input


def parse(lines):
    insts = lines[0]
    graph = {}
    for line in lines[2:]:
        curNode, rest = line.split(" = ")
        left, right = rest[1:-1].split(", ")
        graph[curNode] = (left, right)
    return insts, graph

def findZ(curNode, graph, insts):
    step = 0
    while True:
        for instNum, inst in enumerate(insts):
            step += 1
            curNode = graph[curNode][0 if inst == "L" else 1]

            if curNode[2] == "Z":
                return step


def part1(lines):
    insts, graph = parse(lines)
    # Assumes that AAA -> ZZZ will not encounter other Zs on the way, which seems to be true for these inputs
    return findZ("AAA", graph, insts)


def part2(lines):
    insts, graph = parse(lines)
    # This problem is pretty dumb and the solution does not work for all cases
    return math.lcm(*map(lambda node: findZ(node, graph, insts), filter(lambda x: x[2] == "A", graph)))


lines = read_input(8)
print(part1(lines))
print(part2(lines))
