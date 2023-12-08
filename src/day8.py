# Advent of Code 2023, Day 8
# (c) blu3r4y

import math
from collections import defaultdict

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(data):
    ins, graph = data
    return number_of_steps(ins, graph, "AAA", "ZZZ")


@print_calls
@print_durations(unit="ms")
def part2(data):
    ins, graph = data

    starts = [n for n in graph if n.endswith("A")]
    ends = [n for n in graph if n.endswith("Z")]

    # number of steps from each start to each end
    steps = defaultdict(dict)
    for s in starts:
        for e in ends:
            nsteps = number_of_steps(ins, graph, start=s, end=e)
            if nsteps is not None:
                steps[s][e] = nsteps

    # find the minimum cycle length to reach all ends from all starts
    min_cycle = math.lcm(*(min(steps[k].values()) for k in steps.keys()))
    return min_cycle


def number_of_steps(ins, graph, start="AAA", end="ZZZ"):
    step, curr, visited = 0, start, set()
    while curr != end:
        turn_index = step % len(ins)

        # follow the instruction
        turn = ins[turn_index]
        curr = graph[curr][turn]

        # avoid going in loops
        if (curr, turn_index) in visited:
            return None
        visited.add((curr, turn_index))

        # next step
        step += 1

    return step


def load(data):
    ins, nodes = data.split("\n\n")

    # left and right instructions
    ins_encoder = {"L": 0, "R": 1}
    ins = tuple(ins_encoder[i] for i in ins)

    graph = {}
    for line in nodes.splitlines():
        node, left, right = parse("{:w} = ({:w}, {:w})", line).fixed
        graph[node] = (left, right)

    return ins, graph


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=8)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 16409
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 11795205644011
    puzzle.answer_b = ans2
