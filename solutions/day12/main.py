import functools

from solutions.util import read_input


EMPTY = "."
FIXED = "#"
UNKNOWN = "?"
def parse(lines):
    parsed = []
    for line in lines:
        pattern, runs = line.split()
        parsed.append((pattern, [int(x) for x in runs.split(",")]))
    return parsed
def numValidRuns(pattern, runs):
    runLen = len(runs)
    patternLen = len(pattern)
    @functools.cache
    def validFrom(patternIdx, runIdx):
        if runIdx >= runLen:
            for i in range(patternIdx, patternLen):
                if pattern[i] == FIXED:
                    return 0
            return 1

        nextRun = runs[runIdx]

        if patternIdx > patternLen - nextRun:
            return 0

        c = pattern[patternIdx]
        if c == FIXED:
            if (patternIdx + nextRun) < patternLen and pattern[patternIdx + nextRun] == FIXED:
                return 0
            for i in range(patternIdx, patternIdx + nextRun):
                if pattern[i] == EMPTY:
                    return 0
            return validFrom(patternIdx + nextRun + 1, runIdx + 1)

        elif c == UNKNOWN:
            if (patternIdx + nextRun) < patternLen and pattern[patternIdx + nextRun] == FIXED:
                return validFrom(patternIdx + 1, runIdx)
            for i in range(patternIdx, patternIdx + nextRun):
                if pattern[i] == EMPTY:
                    return validFrom(patternIdx + 1, runIdx) # TODO: I'm not sure why the first arg can't be i + 1

            return validFrom(patternIdx + nextRun + 1, runIdx + 1) + validFrom(patternIdx + 1, runIdx)

        return validFrom(patternIdx + 1, runIdx)

    return validFrom(0, 0)

def part1(lines):
    s = 0
    for pattern, runs in parse(lines):
        s += numValidRuns(pattern, runs)
    return s

def part2(lines):
    s = 0
    for pattern, runs in parse(lines):
        s += numValidRuns(((pattern + UNKNOWN) * 5)[:-1], runs * 5)
    return s

lines = read_input(12)
print(part1(lines))
print(part2(lines))