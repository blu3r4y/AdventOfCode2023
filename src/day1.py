# Advent of Code 2023, Day 1
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations, lfilter


NUMBERS = {
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
        numbers = []
        for i in range(len(line)):
            if line[i].isnumeric():
                numbers.append(line[i])
            for txt, val in NUMBERS.items():
                if line[i:].startswith(txt):
                    numbers.append(val)

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
