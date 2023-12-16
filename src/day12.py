# Advent of Code 2023, Day 12
# (c) blu3r4y

from functools import cache

from aocd.models import Puzzle
from funcy import collecting, lmap, print_calls, print_durations

GAP, MARK, WILDCARD = ".", "#", "?"


@print_calls
@print_durations(unit="ms")
def part1(data):
    total = 0
    for springs, checksum in data:
        total += number_of_arrangements(springs, checksum)

    return total


@print_calls
@print_durations(unit="ms")
def part2(data):
    total = 0
    for springs, checksum in data:
        # unfold by duplicating 5 times and adding wildcards in between
        springs, checksum = (springs + (WILDCARD,)) * 4 + springs, checksum * 5
        total += number_of_arrangements(springs, checksum)

    return total


def number_of_arrangements(springs, checksum):
    return dp(springs + (GAP,), checksum)


@cache
def dp(springs, checksum, open=False):
    symbol, check = springs[0], checksum[0]
    eos, eoc = len(springs) == 1, len(checksum) == 1

    if check < 0:
        return 0

    if symbol == MARK:
        # consume the mark, and continue in open-mode
        return dp(springs[1:], (check - 1,) + checksum[1:], open=True)

    if symbol == GAP:
        if open and check != 0:
            # checksum not reached, fail
            return 0
        if eos:
            # succeed if end of springs and last checksum reached
            return 1 if eoc and check == 0 else 0
        if open:
            # close block, and continue with next checksum
            return dp(springs[1:], (0,) if eoc else checksum[1:], open=False)
        else:
            # skip ahead with same checksum
            return dp(springs[1:], checksum, open=False)

    if symbol == WILDCARD:
        if open:
            if check == 0:
                # close block, and continue with next checksum
                return dp(springs[1:], (0,) if eoc else checksum[1:], open=False)
            else:
                # consume the wildcard, and continue in open-mode
                return dp(springs[1:], (check - 1,) + checksum[1:], open=True)

        else:  # branch
            # either start a new block or skip ahead with same checksum
            a = dp(springs[1:], (check - 1,) + checksum[1:], open=True)
            b = dp(springs[1:], checksum, open=False)
            return a + b


@collecting
def load(data):
    for line in data.split("\n"):
        springs, checksum = line.split(" ")
        checksum = lmap(int, checksum.split(","))
        yield tuple(springs), tuple(checksum)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=12)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 7047
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 17391848518844
    puzzle.answer_b = ans2
