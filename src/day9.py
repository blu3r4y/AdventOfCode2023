# Advent of Code 2023, Day 9
# (c) blu3r4y

import numpy as np
from aocd.models import Puzzle
from funcy import collecting, lmap, print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(histories):
    return sum_predictions(histories)


@print_calls
@print_durations(unit="ms")
def part2(histories):
    return sum_predictions(histories, invert=True)


def sum_predictions(histories, invert=False):
    total = 0
    for history in histories:
        history = history[::-1] if invert else history
        total += extrapolate(history)

    return total


def extrapolate(numbers):
    diffs, offset = np.array(numbers, dtype=int), 0
    while np.count_nonzero(diffs) > 0:
        diffs = np.diff(diffs)
        offset += diffs[-1]

    return numbers[-1] + offset


@collecting
def load(data):
    for line in data.split("\n"):
        yield lmap(int, line.split(" "))


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=9)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 1974913025
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 884
    puzzle.answer_b = ans2
