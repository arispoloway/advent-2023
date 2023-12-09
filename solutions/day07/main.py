import functools
import math
from solutions.util import read_input

from collections import Counter


FIVE = 0
FOUR = 1
FULL = 2
THREE = 3
TWO_PAIR = 4
ONE_PAIR = 5
HIGH_CARD = 6


def handType(hand, useJokers = False):
    counts = Counter(hand)

    jokers = 0
    if useJokers:
        jokers = counts["J"]
        del counts["J"]
        if jokers == 5:
            return FIVE

    freqs = counts.most_common(5)
    freqs[0] = (freqs[0][0], freqs[0][1] + jokers)

    if len(freqs) == 1:
        return FIVE
    if len(freqs) == 5:
        return HIGH_CARD
    if len(freqs) == 4:
        return ONE_PAIR
    if freqs[0][1] == 4:
        return FOUR
    if freqs[0][1] == 3:
        if freqs[1][1] == 2:
            return FULL
        return THREE
    return TWO_PAIR


def handComparator(useJokers):
    elems = "AKQT98765432J" if useJokers else "AKQJT98765432"

    def comparator(hand1, hand2):
        type1 = handType(hand1[0], useJokers)
        type2 = handType(hand2[0], useJokers)
        if type1 < type2:
            return -1
        if type1 > type2:
            return 1
        for (c1, c2) in zip(hand1[0], hand2[0]):
            idx1 = elems.index(c1)
            idx2 = elems.index(c2)
            if idx1 < idx2:
                return -1
            if idx1 > idx2:
                return 1
        return 0
    return comparator


def parse(line):
    s = line.split()
    return (s[0], int(s[1]))


def part1(lines):
    score = 0
    hands = list(map(parse, lines))
    hands.sort(key=functools.cmp_to_key(handComparator(False)), reverse=True)
    for i, line in enumerate(hands):
        score += (i + 1) * line[1]
    return score


def part2(lines):
    score = 0
    hands = list(map(parse, lines))
    hands.sort(key=functools.cmp_to_key(handComparator(True)), reverse=True)
    for i, line in enumerate(hands):
        score += (i + 1) * line[1]
    return score


lines = read_input(7)
print(part1(lines))
print(part2(lines))