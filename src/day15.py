# Advent of Code 2023, Day 15
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(steps):
    total = 0
    for step in steps:
        total += compute_hash(step)

    return total


@print_calls
@print_durations(unit="ms")
def part2(steps):
    boxes = [[] for _ in range(256)]
    lenses = [{} for _ in range(256)]

    for step in steps:
        op, label, lens = parse_step(step)
        box = compute_hash(label)

        # remove label from box if present
        if op == "-":
            if label in boxes[box]:
                boxes[box].remove(label)
                del lenses[box][label]

        # add or replace label in box
        if op == "=":
            lenses[box][label] = lens
            if label not in boxes[box]:
                boxes[box].append(label)

    return compute_focusing_power(boxes, lenses)


def compute_hash(text):
    num = 0
    for c in text:
        num = ((num + ord(c)) * 17) % 256

    return num


def compute_focusing_power(boxes, lenses):
    power = 0
    for b, box in enumerate(boxes):
        for s, slot in enumerate(box, 1):
            power += (b + 1) * s * lenses[b][slot]

    return power


def parse_step(step):
    if step.endswith("-"):
        return "-", step[:-1], 0

    part = step.split("=")
    return "=", part[0], int(part[1])


def load(data):
    return data.split(",")


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=15)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 514025
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 244461
    puzzle.answer_b = ans2
