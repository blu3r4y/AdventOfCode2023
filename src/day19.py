# Advent of Code 2023, Day 19
# (c) blu3r4y

from collections import namedtuple
from functools import reduce
from operator import __ge__, __gt__, __le__, __lt__, mul

from aocd.models import Puzzle
from funcy import print_calls, print_durations

Rule = namedtuple("Rule", ["key", "op", "val", "nxt"])

IN_WORKFLOW, ACCEPT, REJECT = "in", "A", "R"
INVERSE_OPERATORS = {
    __lt__: __ge__,
    __le__: __gt__,
    __gt__: __le__,
    __ge__: __lt__,
}


@print_calls
@print_durations(unit="ms")
def part1(data):
    workflows, parts = data

    total_rating = 0
    for part in parts:
        if is_part_accepted(part, workflows):
            total_rating += sum(part.values())

    return total_rating


@print_calls
@print_durations(unit="ms")
def part2(data):
    workflows, _ = data

    intervals = {k: (1, 4001) for k in "xmas"}
    return number_of_accepts(IN_WORKFLOW, workflows, intervals)


def is_part_accepted(part, workflows):
    nxt = IN_WORKFLOW
    while nxt != ACCEPT and nxt != REJECT:
        for rule in workflows[nxt]:
            if rule.key is None or rule.op(part[rule.key], rule.val):
                nxt = rule.nxt
                break

    return nxt == ACCEPT


def number_of_accepts(flow, workflows, intervals):
    num_accepts = 0

    for rule in workflows[flow]:
        is_terminal = rule.key is None

        # as long as this is not a terminal rule, clamp the interval
        # to the current rule's condition, and recurse on that branch later
        branch_interval = intervals
        if not is_terminal:
            branch_interval = intervals.copy()
            branch_interval[rule.key] = clamp(*intervals[rule.key], rule)

        # compute combinations or recurse
        if rule.nxt == ACCEPT:
            num_accepts += number_of_combinations(branch_interval)
        elif rule.nxt != REJECT:
            num_accepts += number_of_accepts(rule.nxt, workflows, branch_interval)

        # before continuing with the next rule, invert the interval
        # to exclude the current rule's condition that was just processed
        if not is_terminal:
            intervals[rule.key] = clamp(*intervals[rule.key], rule, invert=True)

    return num_accepts


def number_of_combinations(intervals):
    return reduce(mul, ((b - a) for a, b in intervals.values()))


def clamp(a, b, rule: Rule, invert=False):
    op = rule.op if not invert else INVERSE_OPERATORS[rule.op]

    if op == __lt__:
        a, b = a, min(b, rule.val)
    elif op == __le__:
        a, b = a, min(b, rule.val + 1)
    elif op == __gt__:
        a, b = max(a, rule.val + 1), b
    elif op == __ge__:
        a, b = max(a, rule.val), b
    else:
        raise ValueError(f"unknown operator: {op}")

    return (a, b) if a < b else (0, 0)


def load(data):
    a, b = data.split("\n\n")

    workflows = {}
    for line in a.splitlines():
        name, rulelist = line[:-1].split("{")

        rules = []
        for rule in rulelist.split(","):
            # parse a terminal (default) rule
            if ":" not in rule:
                rules.append(Rule(key=None, op=None, val=None, nxt=rule))
                continue

            # parse the condition
            condition, nxt = rule.split(":")
            if "<" in condition:
                key, val = condition.split("<")
                rules.append(Rule(key=key, op=__lt__, val=int(val), nxt=nxt))
            elif ">" in condition:
                key, val = condition.split(">")
                assert not key.isnumeric()
                rules.append(Rule(key=key, op=__gt__, val=int(val), nxt=nxt))
            else:
                raise ValueError(f"unknown condition: {condition}")

        workflows[name] = rules

    parts = []
    for line in b.splitlines():
        fields = {}
        for rule in line[1:-1].split(","):
            name, val = rule.split("=")
            fields[name] = int(val)
        parts.append(fields)

    return workflows, parts


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=19)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 331208
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 121464316215623
    puzzle.answer_b = ans2
