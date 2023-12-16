import functools
from solutions.util import read_input

from collections import defaultdict, OrderedDict

def h(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v

def part1(lines):
    return sum(h(chunk) for chunk in lines[0].split(","))

def part2(lines):
    boxes = defaultdict(OrderedDict)
    for chunk in lines[0].split(","):
        if chunk[-1] == "-":
            txt = chunk[:-1]
            hsh = h(txt)
            if txt in boxes[hsh]:
                del boxes[hsh][txt]
        else:
            txt, val = chunk.split("=")
            val = int(val)
            hsh = h(txt)
            boxes[hsh][txt] = val
    pass

    s = 0
    for box, contents in boxes.items():
        for i, c in enumerate(contents.values()):
            s += (box + 1) * (i+1) * c
    return s

lines = read_input(15)
print(part1(lines))
print(part2(lines))