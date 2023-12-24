# Advent of Code 2023, Day 24
# (c) blu3r4y

from itertools import combinations

from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations
from sympy import ZZ, Symbol, solve


@print_calls
@print_durations(unit="ms")
def part1(traces, test_area=(200000000000000, 400000000000000)):
    lo, hi = test_area
    collisions = 0

    for a, b in combinations(traces, 2):
        (ax, ay, _), (avx, avy, _) = a
        (bx, by, _), (bvx, bvy, _) = b

        # check at what point the two lines intersect, if they do
        if p := intersection(ax, ay, ax + avx, ay + avy, bx, by, bx + bvx, by + bvy):
            px, py = p

            # are the intersection points in the future?
            a_positive = (px - ax) / avx > 0
            b_positive = (px - bx) / bvx > 0

            # are the intersection points within the test area?
            within_test_area = lo <= px <= hi and lo <= py <= hi

            if a_positive and b_positive and within_test_area:
                collisions += 1

    return collisions


@print_calls
@print_durations(unit="ms")
def part2(traces, sample_size=3, check=False):
    # overall, we only have 6 unknowns (3x rock position, 3x rock velocity)
    # plus one unknown for every trace (the time of collision), while every
    # trace adds 3 new equations (x, y, z) to the system. this means that
    # we only need to check 3 traces to have a solvable system of equations,
    # because that gives us 6 + 3 = 9 unknowns and 3 * 3 = 9 equations.

    pre = None
    for i in range(0, len(traces), sample_size):
        result = solve_equations(traces[i : i + sample_size])
        if not check:
            return result

        # check if all the other samples would yield the same result
        assert pre is None or result == pre, f"sample size too small"
        pre = result

    return pre


def intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # intersection of two lines, given by two points each
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

    xnom = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    xdenom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    ynom = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ydenom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # return result or None for parallel lines (denominator is zero)
    return (xnom / xdenom, ynom / ydenom) if xdenom != 0 and ydenom != 0 else None


def solve_equations(traces):
    # rock position and velocity
    rx, ry, rz = (Symbol(x, domain=ZZ) for x in ("rx", "ry", "rz"))
    rvx, rvy, rvz = (Symbol(x, domain=ZZ) for x in ("rvx", "rvy", "rvz"))

    equations = []
    for i, trace in enumerate(traces):
        (x, y, z), (vx, vy, vz) = trace
        t = Symbol(f"t{i}", positive=True, domain=ZZ)

        eqx = rx + t * rvx - x - t * vx
        eqy = ry + t * rvy - y - t * vy
        eqz = rz + t * rvz - z - t * vz
        equations.extend([eqx, eqy, eqz])

    solutions = solve(equations, dict=True, domain=ZZ, check=False)
    assert len(solutions) == 1

    return solutions[0][rx] + solutions[0][ry] + solutions[0][rz]


@collecting
def load(data):
    for line in data.split("\n"):
        pos, vel = line.split(" @ ")
        pos = tuple(map(int, pos.split(", ")))
        vel = tuple(map(int, vel.split(", ")))
        yield (pos, vel)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=24)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 25810
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 652666650475950
    puzzle.answer_b = ans2
