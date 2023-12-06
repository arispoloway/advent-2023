from collections import defaultdict

from solutions.util import read_input


def part1(lines):
    seeds = map(int, lines[0].split(": ")[1].split())

    # dest, source, maps
    maps = []

    curMap = None
    for line in lines[2:]:
        if curMap is None:
            curMap = []
        elif line == "":
            maps.append(curMap)
            curMap = None
        else:
            curMap.append(tuple(map(int, line.split())))
    maps.append(curMap)

    minSeed = 99999999999999999
    for seed in seeds:
        for m in maps:
            for line in m:
                destIdx, sourceIdx, rang = line
                if sourceIdx <= seed < sourceIdx + rang:
                    seed = seed - sourceIdx + destIdx
                    break
        if seed < minSeed:
            minSeed = seed

    return minSeed


def part2(lines):
    seeds = map(int, lines[0].split(": ")[1].split())
    itemRanges = list(zip(*(iter(seeds),) * 2))

    # source, dest, maps
    maps = []

    curMap = None
    for line in lines[2:]:
        if curMap is None:
            curMap = []
        elif line == "":
            maps.append(curMap)
            curMap = None
        else:
            x = tuple(map(int, line.split()))
            curMap.append((x[1], x[0], x[2]))
    maps.append(curMap)
    for m in maps:
        m.sort(key=lambda x: x[0])

    for m in maps:
        newItemRanges = []
        for itemRange in itemRanges:
            itemSourceIdx, itemSourceRange = itemRange

            lineIdx = 0
            done = False
            while lineIdx < len(m):
                if itemSourceRange == 0:
                    done = True
                    break
                sourceIdx, destIdx, mapRange = m[lineIdx]

                if itemSourceIdx < sourceIdx:
                    if (itemSourceIdx + itemSourceRange) <= sourceIdx:
                        newItemRanges.append((itemSourceIdx, itemSourceRange))
                        done = True
                        break
                    else:
                        beforeRange = sourceIdx - itemSourceIdx
                        newItemRanges.append((itemSourceIdx, beforeRange))
                        itemSourceRange -= beforeRange
                        itemSourceIdx = sourceIdx
                elif itemSourceIdx < (sourceIdx + mapRange):
                    if (itemSourceIdx + itemSourceRange) <= (sourceIdx + mapRange):
                        newItemRanges.append((itemSourceIdx - sourceIdx + destIdx, itemSourceRange))
                        done = True
                        break
                    else:
                        beforeRange = (sourceIdx + mapRange) - itemSourceIdx
                        newItemRanges.append((itemSourceIdx - sourceIdx + destIdx, beforeRange))
                        itemSourceRange -= beforeRange
                        itemSourceIdx = sourceIdx + mapRange
                        lineIdx += 1
                else:
                    lineIdx += 1
            if not done and itemSourceRange != 0:
                newItemRanges.append((itemSourceIdx, itemSourceRange))
        itemRanges = newItemRanges
    return min(map(lambda x: x[0], itemRanges))


lines = read_input(5)
print(part1(lines))
print(part2(lines))
