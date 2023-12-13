# Advent of Code 2023, Day 13
# (c) blu3r4y

import numpy as np
from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(grid):
    return solve(grid, 0)


@print_calls
@print_durations(unit="ms")
def part2(grid):
    return solve(grid, 1)


def solve(grid, num_smudges):
    total = 0
    for block in grid:
        if x := find_reflection(block, num_smudges):
            total += x
        if y := find_reflection(block.T, num_smudges):
            total += 100 * y

    return total


def find_reflection(block, num_smudges=0):
    # find vertical reflection, i.e., return the mirror's column index
    size = block.shape[1]
    for x in range(1, size):
        # reflection is bounded by the shorter side
        reflection_length = min(x + x, size) - x

        left = block[:, x - reflection_length : x]
        right = np.fliplr(block[:, x : x + reflection_length])

        # look for perfect reflection (num_smudges=0)
        # or allow for a number of mismatches
        smudges = np.sum(left != right)
        if smudges == num_smudges:
            return x


@collecting
def load(data):
    mapping = {".": 0, "#": 1}
    for block in data.split("\n\n"):
        rows = block.split("\n")
        rows = [[mapping[cell] for cell in row] for row in rows]
        yield np.array(rows, dtype=int)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=13)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 31877
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 42996
    puzzle.answer_b = ans2
