# Advent of Code 2023, Day 21
# (c) blu3r4y

import numpy as np
from aocd.models import Puzzle
from funcy import print_calls, print_durations
from scipy.interpolate import CubicSpline

START, GARDEN, ROCK = "S", ".", "#"


@print_calls
@print_durations(unit="ms")
def part1(data, nsteps=64):
    rocks, bounds, start = data

    # only extract the number of reachable blocks in the last step
    *_, num_reachable = reachable_blocks(nsteps, rocks, bounds, start)
    return num_reachable


@print_calls
@print_durations(unit="ms")
def part2(data, nsteps=26501365):
    rocks, bounds, start = data

    period_start = int(start.real)
    period_length = bounds[0]

    # after careful manual analysis of the lagplots, it turns out
    # that the number of reachable blocks is periodic with
    # period 131 (grid size), and offset 65 (start position)
    assert (nsteps - period_start) % period_length == 0

    # compute the steps to get three data points
    history = reachable_blocks(period_start + 2 * period_length, rocks, bounds, start)

    # interpolate a cubic spline; though, it is probably just quadratic ...
    ys = np.array(history[period_start - 1 :: period_length])
    xs = np.arange(len(ys))
    spline = CubicSpline(xs, ys)

    # evaluate the spline at the desired position
    target_period = (nsteps - period_start) // period_length
    return int(spline(target_period))


def reachable_blocks(nsteps, rocks, bounds, start):
    fringe, history = {start}, []
    for _ in range(nsteps):
        reachable = set()

        while fringe:
            cell = fringe.pop()
            for succ in successors(cell, rocks, bounds):
                reachable.add(succ)

        fringe = reachable
        history.append(len(fringe))

    return history


def successors(pos, rocks, bounds):
    for delta in (1, -1, 1j, -1j):
        nxt = pos + delta
        infnxt = complex(nxt.real % bounds[1], nxt.imag % bounds[0])
        if infnxt not in rocks:
            yield nxt


def load(data):
    lines = data.split("\n")

    bounds = len(lines), len(lines[0])
    rocks, start = set(), None

    for y, line in enumerate(lines):
        for x, cell in enumerate(line):
            if cell == ROCK:
                rocks.add(x + y * 1j)
            elif cell == START:
                start = x + y * 1j

    return rocks, bounds, start


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=21)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 3751
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 619407349431167
    puzzle.answer_b = ans2
