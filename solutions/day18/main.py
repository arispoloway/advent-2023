import functools
import queue

from solutions.util import read_input, withinGrid

from collections import defaultdict, OrderedDict



def parse(lines):
    out = []

    for line in lines:
        dir, amount, color = line.split()
        out.append((dir, int(amount), color[2:-1]))

    return out

def move(pos, direction):
    x, y = pos
    dx, dy = direction
    return x + dx, y + dy

def dir(dirStr, amount):
    if dirStr == "U":
        return (0, -amount)
    if dirStr == "D":
        return (0, amount)
    if dirStr == "L":
        return (-amount, 0)
    if dirStr == "R":
        return (amount, 0)


# Given the vertical lines making up the shape, and a y coordinate, determine how volume is used in that specific row
def rowScore(y, verticalLines):
    rowScore = 0

    lastX = -999999999
    isOnStart = False
    isOnEnd = False
    inRegion = False
    inRegionBefore = False

    for lineX, (lineYStart, lineYEnd) in verticalLines:
        if not lineYStart <= y <= lineYEnd:
            continue

        willBeOnStart = y == lineYStart
        willBeOnEnd = y == lineYEnd

        if not inRegion:
            inRegion = True
            isOnStart = willBeOnStart
            isOnEnd = willBeOnEnd
            inRegionBefore = False
            lastX = lineX
        else:
            if (isOnStart and willBeOnStart) or (isOnEnd and willBeOnEnd):
                if not inRegionBefore:
                    inRegion = False
                    rowScore += lineX - lastX + 1
                isOnStart = False
                isOnEnd = False
                inRegionBefore = False
            elif (isOnStart and willBeOnEnd) or (isOnEnd and willBeOnStart):
                if inRegionBefore:
                    inRegion = False
                    inRegionBefore = False
                    rowScore += lineX - lastX + 1

                isOnStart = False
                isOnEnd = False
            elif willBeOnStart or willBeOnEnd:
                inRegionBefore = True
                isOnStart = willBeOnStart
                isOnEnd = willBeOnEnd
            else:
                rowScore += lineX - lastX + 1
                inRegion = False
                inRegionBefore = False
    return rowScore


# assuming only 4 cardinal directions, we can calculate the space by going down each row, and going left to right over
# each vertical line, determining if we are in or out of the space as we cross each
# This basically does that which is somewhat messy, but has the slight optimization that it only looks at y values
# around where lines start and end, since in between it'll be identical, and we can just multiply an individual row's
# contribution by the number of times it's repeated
def filledSpace(verticalLines):
    verticalLines.sort()

    yCoords = []
    for _, (startY, endY) in verticalLines:
        yCoords.append(startY-1)
        yCoords.append(startY)
        yCoords.append(startY+1)
        yCoords.append(endY-1)
        yCoords.append(endY)
        yCoords.append(endY+1)
    yCoords.sort()

    score = 0
    lastYCoord = 0
    lastRowScore = 0

    for y in yCoords:
        newRowScore = rowScore(y, verticalLines)
        score += lastRowScore * (y - lastYCoord)
        lastYCoord = y
        lastRowScore = newRowScore

    return score

def part1(lines):
    actions = parse(lines)

    pos = (0, 0)

    # (Column, (row start, row end))
    verticalLines = []

    for dirStr, amount, _ in actions:
        d = dir(dirStr, amount)
        startPos = pos
        pos = move(pos, d)
        if dirStr == "U":
            verticalLines.append((pos[0], (pos[1], startPos[1])))
        if dirStr == "D":
            verticalLines.append((pos[0], (startPos[1], pos[1])))

    return filledSpace(verticalLines)



def part2(lines):
    actions = parse(lines)
    pos = (0, 0)
    # (Column, (row start, row end))
    verticalLines = []
    for _, _, c in actions:
        amount = int(c[:-1], 16)
        dirStr = ["R", "D", "L", "U"][int(c[-1])]
        d = dir(dirStr, amount)
        startPos = pos
        pos = move(pos, d)
        if dirStr == "U":
            verticalLines.append((pos[0], (pos[1], startPos[1])))
        if dirStr == "D":
            verticalLines.append((pos[0], (startPos[1], pos[1])))

    return filledSpace(verticalLines)


lines = read_input(18)
print(part1(lines))
print(part2(lines))