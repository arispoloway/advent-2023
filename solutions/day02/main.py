from collections import defaultdict

from solutions.util import read_input


def parse_games(lines):
    games = {}

    for i, line in enumerate(lines):
        sets = []
        for set in line.split(": ")[1].split("; "):
            curset = defaultdict(lambda: 0)
            for take in set.strip().split(", "):
                sep = take.split(" ")
                curset[sep[1]] = int(sep[0])
            sets.append(curset)

        games[i + 1] = sets
    return games


def part1(lines):
    games = parse_games(lines)
    s = 0
    for id, game in games.items():
        valid = True
        for set in game:
            if not (set["red"] <= 12 and set["green"] <= 13 and set["blue"] <= 14):
                valid = False
                break
        if valid:
            s += id

    return s


def part2(lines):
    games = parse_games(lines)
    s = 0
    for _, game in games.items():
        mins = defaultdict(lambda: 0)
        for set in game:
            for color, num in set.items():
                if mins[color] < num:
                    mins[color] = num
        prod = 1
        for num in mins.values():
            prod = prod * num
        s += prod
    return s


lines = read_input(2)
print("day02")
print(part1(lines))
print(part2(lines))
