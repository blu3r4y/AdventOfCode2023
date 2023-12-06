# Advent of Code 2023, Day 6
# (c) blu3r4y

from math import sqrt, ceil, floor

from aocd.models import Puzzle
from funcy import print_calls, print_durations, lmap
from parse import parse


def compute_number_of_ways(t, d):
    h1 = 1 / 2 * (t - sqrt(t**2 - 4 * d))
    h2 = 1 / 2 * (t + sqrt(t**2 - 4 * d))

    eps = 1e-10  # add some epsilon to respect inequalities
    nways = floor(h2 - eps) - ceil(h1 + eps) + 1
    return nways


@print_calls
@print_durations(unit="ms")
def part1(data):
    times, dists = data

    product = 1
    for t, d in zip(times, dists):
        product *= compute_number_of_ways(t, d)

    return product


@print_calls
@print_durations(unit="ms")
def part2(data):
    times, dists = data
    t = int("".join(map(str, times)))
    d = int("".join(map(str, dists)))

    return compute_number_of_ways(t, d)


def load(data):
    times, dists = data.split("\n")
    times = lmap(int, parse("Time: {}", times)[0].split())
    dists = lmap(int, parse("Distance: {}", dists)[0].split())

    return times, dists


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=6)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 2374848
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 39132886
    puzzle.answer_b = ans2
