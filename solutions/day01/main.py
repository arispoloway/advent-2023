from solutions.util import read_input



def part1(lines):
    s = 0
    for line in lines:
        nums = [c for c in line if c in "0123456789"]
        s += int(nums[0] + nums[-1])
    return s

def part2(lines):
    repls = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9
    }

    s = 0
    for line in lines:

        nums = []
        for i, c in enumerate(line):
            if c in "0123456789":
                nums.append(int(c))
            for repl, new in repls.items():
                if line[i:i+len(repl)] == repl:
                    nums.append(new)

        s += 10*nums[0] + nums[-1]
    return s


lines = read_input(1)
print(part1(lines))
print(part2(lines))

