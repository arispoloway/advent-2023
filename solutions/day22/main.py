from collections import defaultdict

from solutions.util import read_input, withinGrid

def brickPositions(start, end):
    x, y, z = start
    x2, y2, z2 = end
    if x < x2:
        return [(i, y, z) for i in range(x, x2+1)]
    if x > x2:
        return [(i, y, z) for i in range(x2, x + 1)]
    if y < y2:
        return [(x, i, z) for i in range(y, y2 + 1)]
    if y > y2:
        return [(x, i, z) for i in range(y2, y + 1)]
    if z < z2:
        return [(x, y, i) for i in range(z, z2 + 1)]
    if z > z2:
        return [(x, y, i) for i in range(z2, z + 1)]
    return [start]

def parse(lines):
    bricks = []
    for i, line in enumerate(lines):
        start, end = line.split("~")
        start = tuple(int(n) for n in start.split(","))
        end = tuple(int(n) for n in end.split(","))
        bricks.append((start, end, i + 1))
    return bricks

# TODO just return a propery dag implementation instead of this thing
def getSupports(bricks):
    bricks.sort(key=lambda b: min(b[0][2], b[1][2]))

    # x -> y -> list( tuple(z, name) )
    fallenBricks = defaultdict(lambda: defaultdict(list))

    for brick in bricks:
        minZ = 1
        for position in brickPositions(brick[0], brick[1]):
            x, y, z = position
            existingBricks = fallenBricks[x][y]
            if len(existingBricks) != 0:
                minZ = max(minZ, existingBricks[-1][0] + 1)

        if brick[0][2] != brick[1][2]:
            for i, position in enumerate(brickPositions(brick[0], brick[1])):
                x, y, _ = position
                fallenBricks[x][y].append((minZ + i, brick[2]))
        else:
            for position in brickPositions(brick[0], brick[1]):
                x, y, _ = position
                fallenBricks[x][y].append((minZ, brick[2]))

    supports = {}
    supportedBy = {}
    for brick in bricks:
        supports[brick[2]] = set()
        supportedBy[brick[2]] = set()

    for ys in fallenBricks.values():
        for zs in ys.values():
            for i, (z, name) in enumerate(zs[:-1]):
                if z == zs[i + 1][0] - 1 and name != zs[i + 1][1]:
                    supports[name].add(zs[i + 1][1])
                    supportedBy[zs[i + 1][1]].add(name)
    return supports, supportedBy


def part1(lines):
    bricks = parse(lines)
    supports, supportedBy = getSupports(bricks)

    count = 0
    for brick in bricks:
        name = brick[2]
        # If everything this brick supports is supported by more than 1 thing, it's safe to remove
        if all(len(supportedBy[support]) > 1 for support in supports[name]):
            count += 1

    return count

def part2(lines):
    bricks = parse(lines)
    supportsC, supportedByC = getSupports(bricks)

    count = 0
    for brick in bricks:
        # There's probably a smarter way than just duplicating it each time...
        supports = {n: set(c) for n, c in supportsC.items()}
        supportedBy = {n: set(c) for n, c in supportedByC.items()}

        name = brick[2]
        c = 0
        toRemove = {name}
        while len(toRemove) != 0:
            c += 1
            n = next(iter(toRemove))
            toRemove.remove(n)

            nSupports = set(supports[n])
            for support in nSupports:
                supportedBy[support].remove(n)
                supports[n].remove(support)
                if len(supportedBy[support]) == 0:
                    toRemove.add(support)

        count += (c - 1)

    return count

lines = read_input(22)
print(part1(lines))
print(part2(lines))
