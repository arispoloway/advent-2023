import functools

from solutions.util import read_input

def parse(lines):
    puzzles = []
    curPuz = []
    for line in lines:
        if line == "":
            puzzles.append(curPuz)
            curPuz = []
        else:
            curPuz.append(line)
    puzzles.append(curPuz)
    return puzzles


def colOffsetErrors(puz, offset):
    errs = 0
    for y in range(len(puz)):
        for i in range(min(len(puz[0]) - offset, offset)):
            if puz[y][offset + i] != puz[y][offset - i - 1]:
                errs += 1
    return errs


def rowOffsetErrors(puz, offset):
    errs = 0
    for x in range(len(puz[0])):
        for i in range(min(len(puz) - offset, offset)):
            if puz[offset + i][x] != puz[offset - i - 1][x]:
                errs += 1
    return errs


def findReflections(puz, idealErrors=0):
    colOffset = None
    rowOffset = None

    for offset in range(1, len(puz[0])):
        if colOffsetErrors(puz, offset) == idealErrors:
            colOffset = offset
        if colOffset is not None:
            break
    for offset in range(1, len(puz)):
        if rowOffsetErrors(puz, offset) == idealErrors:
            rowOffset = offset
        if rowOffset is not None:
            break
    return colOffset, rowOffset


def part1(lines):
    puzzles = parse(lines)
    s = 0
    for puz in puzzles:
        xReflect, yReflect = findReflections(puz)
        if xReflect is not None:
            s += xReflect
        if yReflect is not None:
            s += 100 * yReflect
    return s

def part2(lines):
    puzzles = parse(lines)
    s = 0
    for puz in puzzles:
        xReflect, yReflect = findReflections(puz, 1)
        if xReflect is not None:
            s += xReflect
        if yReflect is not None:
            s += 100 * yReflect
    return s

lines = read_input(13)
print(part1(lines))
print(part2(lines))