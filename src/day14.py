# Advent of Code 2023, Day 14
# (c) blu3r4y

from collections import defaultdict

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, print_durations

EMPTY, ROCK, DISH = 0, 1, 2


@print_calls
@print_durations(unit="ms")
def part1(grid):
    roll_rocks(grid)
    return beam_load(grid)


@print_calls
@print_durations(unit="ms")
def part2(grid, cycles=1000000000):
    cyclecache = defaultdict(int)

    c = 0
    while c < cycles:
        # roll and rotate clockwise 4 times
        for _ in range(4):
            roll_rocks(grid)
            grid = np.rot90(grid, k=-1)

        c += 1

        # check if we have seen this grid before
        # and if so, skip forward close to the end
        key = tuple(grid.ravel())
        if cstart := cyclecache.get(key):
            cycle_length = c - cstart
            n_repeat = (cycles - c) // cycle_length
            if n_repeat > 0:
                c = cstart + n_repeat * cycle_length

        cyclecache[key] = c

    return beam_load(grid)


def roll_rocks(grid):
    nrows, ncols = grid.shape

    for x in range(ncols):
        yfree = 0  # north-most free row

        for y in range(nrows):
            if grid[y, x] == ROCK:
                yfree = y + 1
            elif grid[y, x] == DISH:
                grid[y, x] = EMPTY
                grid[yfree, x] = DISH
                yfree += 1


def beam_load(grid):
    nrows, ncols = grid.shape
    total = 0

    for x in range(ncols):
        cells = enumerate(grid[:, x])
        score = (nrows - i for i, cell in cells if cell == DISH)
        total += sum(score)

    return total


def load(data):
    mapping = {".": EMPTY, "#": ROCK, "O": DISH}
    rows = data.split("\n")
    rows = [[mapping[cell] for cell in row] for row in rows]
    return np.array(rows, dtype=int)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=14)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 106186
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 106390
    puzzle.answer_b = ans2
