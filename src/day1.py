# Advent of Code 2023, Day 1
# (c) blu3r4y

import re

from aocd.models import Puzzle
from funcy import lfilter, print_calls, print_durations

NUMS_REGEX_PATTERN = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
NUMS_REGEX = re.compile(NUMS_REGEX_PATTERN)
NUMS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


@print_calls
@print_durations(unit="ms")
def part1(lines):
    total = 0
    for line in lines:
        line = lfilter(lambda x: x.isnumeric(), line)
        total += int(line[0] + line[-1])

    return total


@print_calls
@print_durations(unit="ms")
def part2(lines):
    total = 0
    for line in lines:
        numbers = NUMS_REGEX.findall(line)
        numbers = [NUMS.get(n, n) for n in numbers]
        total += int(numbers[0] + numbers[-1])

    return total


def load(data):
    return data.split("\n")


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=1)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 54667
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 54203
    puzzle.answer_b = ans2
