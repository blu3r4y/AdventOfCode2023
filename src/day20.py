# Advent of Code 2023, Day 20
# (c) blu3r4y

from collections import defaultdict
from math import lcm

from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(wiring):
    processor = build_processor(wiring)
    for _ in range(1000):
        processor.push_button()

    result = processor.num_pulses[False] * processor.num_pulses[True]
    return result


@print_calls
@print_durations(unit="ms")
def part2(wiring):
    processor = build_processor(wiring)

    # record when the modules of the input of rx's parent get a high pulse
    watch_inputs = processor.inputs[processor.inputs["rx"][0]]
    processor.add_watches(watch_inputs)
    while processor.get_watches() is None:
        processor.push_button()

    # rx is connected to four circles of flip-flops that have very long cycle times.
    # only if all the cycles would fire at the same time, the output of rx would be high.
    # we can't simulate the whole thing, but we can simulate each cycle individually
    # and then find the least common multiple of all the cycles, which is the result.

    result = lcm(*processor.get_watches().values())
    return result


def build_processor(wiring):
    processor = Processor()

    for module_type, module_name, outputs in wiring:
        if module_type == "%":
            processor.add_module(FlipFlop(module_name, outputs, processor))
        elif module_type == "&":
            processor.add_module(Conjunction(module_name, outputs, processor))
        elif module_type == "broadcaster":
            processor.add_module(Broadcast(module_name, outputs, processor))

    processor.wire_inputs()
    return processor


class Processor:
    def __init__(self):
        self.modules = {}
        self.inputs = defaultdict(list)
        self.button_count = 0
        self.num_pulses = {False: 0, True: 0}
        self.watches = {}
        self.watch_modules = set()

    def add_module(self, module):
        self.modules[module.name] = module
        for output in module.outputs:
            self.inputs[output].append(module.name)

    def wire_inputs(self):
        for module in self.modules.values():
            if isinstance(module, Conjunction):
                module.wire_inputs(self.inputs[module.name])

    def add_watches(self, modules):
        self.watch_modules = set(modules)

    def remove_watches(self):
        self.watch_modules = set()

    def get_watches(self):
        if self.watches.keys() == self.watch_modules:
            return self.watches

    def push_button(self):
        # button press sends a low pulse to the broadcaster
        self.modules["broadcaster"].on_receive(False)
        self.num_pulses[False] += 1
        self.button_count += 1

        stack = ["broadcaster"]
        while stack:
            module = self.modules[stack.pop(0)]
            name = module.name

            if (pulse := module.get_output()) is not None:
                # record when a watched module receives a high pulse for the first time
                if pulse and name in self.watch_modules and name not in self.watches:
                    self.watches[name] = self.button_count

                # propagate pulse to all outputs of the module and enqueue them
                for output in module.outputs:
                    self.num_pulses[pulse] += 1
                    if output in self.modules:
                        self.modules[output].on_receive(pulse, source=name)
                        stack.append(output)


class FlipFlop:
    def __init__(self, name, outputs, processor):
        self.name = name
        self.outputs = outputs
        self.processor = processor
        self.state = False
        self.toggled = False

    def on_receive(self, pulse: bool, **kwargs):
        if not pulse:
            self.state = not self.state
            self.toggled = True

    def get_output(self):
        if self.toggled:
            self.toggled = False
            return self.state


class Conjunction:
    def __init__(self, name, outputs, processor):
        self.name = name
        self.outputs = outputs
        self.processor = processor
        self.memory = None

    def wire_inputs(self, inputs):
        self.memory = {e: False for e in inputs}

    def on_receive(self, pulse: bool, source: str):
        self.memory[source] = pulse

    def get_output(self):
        return not all(self.memory.values())


class Broadcast:
    def __init__(self, name, outputs, processor):
        self.name = name
        self.outputs = outputs
        self.processor = processor
        self.state = False

    def on_receive(self, pulse: bool, **kwargs):
        self.state = pulse

    def get_output(self):
        return self.state


@collecting
def load(data):
    for line in data.split("\n"):
        identifier, outputs = line.split(" -> ")
        outputs = outputs.split(", ")

        module_type, module_name = identifier[0], identifier[1:]
        if identifier == "broadcaster":
            module_type, module_name = "broadcaster", "broadcaster"

        yield module_type, module_name, outputs


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=20)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 929810733
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 231657829136023
    puzzle.answer_b = ans2
