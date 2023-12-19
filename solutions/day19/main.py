from solutions.util import read_input


def parse(lines):
    parsingWorkflows = True
    workflows = {}
    objects = []

    for line in lines:
        if line == "":
            parsingWorkflows = False
            continue
        if parsingWorkflows:
            name, ruleStrings = line[:-1].split("{")

            rules = []
            for rule in ruleStrings.split(","):
                if ":" in rule:
                    c, dest = rule.split(":")
                    rules.append(ComparisonRule(c[0], c[1], int(c[2:]), dest))
                else:
                    rules.append(DestinationRule(rule))
            workflows[name] = Workflow(name, rules)
        else:
            obj = {}
            for field in line[1:-1].split(","):
                name, strVal = field.split("=")
                obj[name] = int(strVal)
            objects.append(obj)
    return workflows, objects

class ComparisonRule(object):
    def __init__(self, field, comparison, value, destination):
        self.field = field
        self.comparison = comparison
        self.value = value
        self.destination = destination

    def ranges(self, fromRanges):
        start, end = fromRanges[self.field]
        matchObj = dict(fromRanges)
        notMatchObj = dict(fromRanges)

        if self.comparison == ">":
            if start > self.value:
                return fromRanges, None
            if end <= self.value:
                return None, fromRanges
            matchObj[self.field] = (self.value + 1, end)
            notMatchObj[self.field] = (start, self.value)
            return matchObj, notMatchObj
        else:
            if end < self.value:
                return fromRanges, None
            if start >= self.value:
                return None, fromRanges
            matchObj[self.field] = (start, self.value - 1)
            notMatchObj[self.field] = (self.value, end)
            return matchObj, notMatchObj

class DestinationRule(object):
    def __init__(self, destination):
        self.destination = destination

    def ranges(self, obj):
        return obj, None


class Workflow(object):
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def destinations(self, obj):
        for rule in self.rules:
            matches, obj = rule.ranges(obj)
            if matches is not None:
                yield matches, rule.destination
            if obj is None:
                break


def acceptedCount(workflows, objs):
    accepted = 0

    while len(objs) != 0:
        obj, workflow = objs.pop()
        for obj, dest in workflows[workflow].destinations(obj):
            if dest == "A":
                p = 1
                for start, end in obj.values():
                    p *= (end - start + 1)
                accepted += p
            elif dest == "R":
                pass
            else:
                objs.append((obj, dest))
    return accepted

def isAccepted(workflows, obj):
    rangeObj = {key: (val, val) for key, val in obj.items()}
    return acceptedCount(workflows, [(rangeObj, "in")]) == 1

def part1(lines):
    workflows, objects = parse(lines)
    return sum(sum(obj.values()) for obj in objects if isAccepted(workflows, obj))
def part2(lines):
    workflows, objs = parse(lines)
    obj = next(iter(objs))
    for key in obj:
        obj[key] = (1, 4000)
    objs = [(obj, "in")]
    return acceptedCount(workflows, objs)

lines = read_input(19)
print(part1(lines))
print(part2(lines))