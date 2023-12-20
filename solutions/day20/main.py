import abc
import collections
import math

from solutions.util import read_input


HIGH = True
LOW = False

class Component(abc.ABC):
    @abc.abstractmethod
    def pulse(self, input, p):
        pass

    def reset(self):
        pass

    def addInput(self, input):
        pass


class Broadcaster(Component):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    def pulse(self, _input, p):
        return [(target, p) for target in self.targets]

class FlipFlop(Component):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.state = LOW

    def reset(self):
        self.state = LOW

    def pulse(self, _input, p):
        if p:
            return []
        self.state = not self.state
        return [(target, self.state) for target in self.targets]

class Conjunction(Component):
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.inputStates = {}

    def addInput(self, input):
        self.inputStates[input] = LOW


    def reset(self):
        for input in self.inputStates:
            self.inputStates[input] = LOW

    def pulse(self, input, p):
        self.inputStates[input] = p
        allHigh = all(self.inputStates.values())
        return [(target, not allHigh) for target in self.targets]


def parseComponent(line):
    name, targetStr = line.split(" -> ")
    targets = targetStr.split(", ")
    if name[0] == "%":
        return FlipFlop(name[1:], targets)
    if name[0] == "&":
        return Conjunction(name[1:], targets)
    return Broadcaster(name, targets)


class Computer(object):
    def __init__(self, components):
        self.components = {}

        for component in components:
            self.components[component.name] = component

        for component in components:
            for target in component.targets:
                if target in self.components:
                    self.components[target].addInput(component.name)
    def reset(self):
        for component in self.components.values():
            component.reset()

    def pulse(self, p, target = "broadcaster", trackInputs = None):
        pulses = collections.deque()
        pulses.append(("button", target, p))

        high = 0
        low = 0
        hits = set()
        while len(pulses) != 0:
            source, target, p = pulses.popleft()
            if p:
                high += 1
            else:
                low += 1
            if target in self.components:
                for newTarget, pulse in self.components[target].pulse(source, p):
                    pulses.append((target, newTarget, pulse))

            if trackInputs is not None:
                for name, inputState in self.components[trackInputs].inputStates.items():
                    if inputState:
                        hits.add(name)

        return low, high, hits

def parse(lines):
    components = [parseComponent(line) for line in lines]
    return Computer(components)

def part1(lines):
    computer = parse(lines)
    lowCount = 0
    highCount = 0

    for _ in range(1000):
        low, high, _ = computer.pulse(LOW)
        lowCount += low
        highCount += high

    return lowCount * highCount


# The solution here relies on a special input, where the final section is fed to by 4 looping subcomponents.
# Ultimately I'm not a fan of this, as you needed to look at the input to realize this.
def part2(lines):
    computer = parse(lines)
    final = None
    for component in computer.components.values():
        if "rx" in component.targets:
            final = component.name
            break

    lcm = 1
    allHits = set()
    for i in range(1, 50_000):
        _, _, hits = computer.pulse(LOW, trackInputs=final)
        if len(hits) != 0:
            allHits = allHits.union(hits)
            lcm = math.lcm(lcm, i)
            if len(allHits) == len(computer.components[final].inputStates):
                return lcm

lines = read_input(20)
print(part1(lines))
print(part2(lines))