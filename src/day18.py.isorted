# Advent of Code 2023, Day 18
# (c) blu3r4y

from collections import namedtuple

from aocd.models import Puzzle
from funcy import pairwise, print_calls, print_durations
from parse import parse

Ins = namedtuple("Ins", ["action", "value"])


@print_calls
@print_durations(unit="ms")
def part1(plan):
    return trench_area(plan)


@print_calls
@print_durations(unit="ms")
def part2(plan):
    return trench_area(plan)


def trench_area(plan):
    vert, length = trench_vertices(plan)

    vert = [(int(z.real), int(z.imag)) for z in vert]
    area = compute_positive_polygon_area(vert)
    points = compute_points_inside_polygon(area, length)

    # inner area plus edge length
    return points + length


def trench_vertices(plan):
    vert, length = [0], 0

    # compute the vertices of the trench
    # and sum the total lenght of the edge
    for ins in plan:
        length += ins.value
        match ins.action:
            case "R":
                vert.append(vert[-1] - ins.value)
            case "L":
                vert.append(vert[-1] + ins.value)
            case "U":
                vert.append(vert[-1] - ins.value * 1j)
            case "D":
                vert.append(vert[-1] + ins.value * 1j)

    return vert, length


def compute_positive_polygon_area(vert):
    if (area := compute_polygon_area(vert)) >= 0:
        return area

    # if the vertices were not given in counter-clockwise order,
    # the result will be negative, so reverse and try again
    return compute_polygon_area(vert[::-1])


def compute_polygon_area(vert):
    area = 0

    # Triangle formula to compute area of a polygon
    # https://en.m.wikipedia.org/wiki/Shoelace_formula#Triangle_formula
    for (x1, y1), (x2, y2) in pairwise(vert + [vert[0]]):
        area += x1 * y2 - x2 * y1

    return area / 2


def compute_points_inside_polygon(area, num_edges):
    # Pick's theorem to compute the inner points of a grid-based polygon
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return int(area - num_edges / 2 + 1)


def load(data, decode_hex=False):
    action_map = {"0": "R", "1": "D", "2": "L", "3": "U"}

    plan = []
    for line in data.split("\n"):
        action, meters, color = parse("{} {:d} (#{})", line)
        if decode_hex:
            meters = int(color[:5], 16)
            action = action_map[color[5]]
        plan.append(Ins(action, meters))

    return plan


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=18)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 95356
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data, decode_hex=True))
    assert ans2 == 92291468914147
    puzzle.answer_b = ans2
