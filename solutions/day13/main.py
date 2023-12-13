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


def colOffsetErrors(puz, offset, maxErrors = 1):
    errs = 0
    for y in range(len(puz)):
        for i in range(min(len(puz[0]) - offset, offset)):
            if puz[y][offset + i] != puz[y][offset - i - 1]:
                errs += 1
        if errs > maxErrors:
            return errs
    return errs


def rowOffsetErrors(puz, offset, maxErrors = 1):
    errs = 0
    for x in range(len(puz[0])):
        for i in range(min(len(puz) - offset, offset)):
            if puz[offset + i][x] != puz[offset - i - 1][x]:
                errs += 1
            if errs > maxErrors:
                return errs
    return errs

def findXReflection(puz, idealErrors=0):
    for offset in range(1, len(puz[0])):
        if colOffsetErrors(puz, offset) == idealErrors:
            return offset
    return 0
def findYReflection(puz, idealErrors=0):
    for offset in range(1, len(puz)):
        if rowOffsetErrors(puz, offset) == idealErrors:
            return offset
    return 0
def part1(lines):
    return sum(findXReflection(puz) + 100 * findYReflection(puz) for puz in parse(lines))

def part2(lines):
    return sum(findXReflection(puz, 1) + 100 * findYReflection(puz, 1) for puz in parse(lines))

lines = read_input(13)
print(part1(lines))
print(part2(lines))