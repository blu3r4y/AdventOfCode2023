# Advent of Code 2023, Day 22
# (c) blu3r4y

from collections import defaultdict

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse

X, Y, Z = 0, 1, 2
STA, END = 0, 1


@print_calls
@print_durations(unit="ms")
def part1(bricks):
    is_supported_by, _ = simulate_gravity(bricks)
    essential_bricks = essential_brick_indexes(is_supported_by)
    return len(bricks) - len(essential_bricks)


@print_calls
@print_durations(unit="ms")
def part2(bricks):
    is_supported_by, does_support = simulate_gravity(bricks)
    essential_bricks = essential_brick_indexes(is_supported_by)

    total_fallen_bricks = 0
    for b in essential_bricks:
        total_fallen_bricks += num_supported_bricks(b, is_supported_by, does_support)

    return total_fallen_bricks


def simulate_gravity(bricks):
    is_supported_by = defaultdict(set)  # key "is supported by" values
    does_support = defaultdict(set)  # key "does support" values

    # iterate bricks, sorted by their highest point in z
    bricks = sorted(bricks, key=lambda b: b[END][Z])
    for i in range(len(bricks)):
        this = bricks[i]

        # the xy coordinates of that brick to be
        # checked for supporting bricks below them
        this_xy = set()
        for x in range(this[STA][X], this[END][X] + 1):
            for y in range(this[STA][Y], this[END][Y] + 1):
                this_xy.add((x, y))

        # identify what bricks are below the current brick,
        # indexed by their highest z coordinate
        below_bricks = defaultdict(set)
        for j, other in enumerate(bricks[:i]):
            if other[END][Z] >= this[STA][Z]:
                continue

            for x in range(other[STA][X], other[END][X] + 1):
                for y in range(other[STA][Y], other[END][Y] + 1):
                    if (x, y) in this_xy:
                        below_bricks[other[END][Z]].add(j)
                        break  # continue outer loop, next brick
                else:
                    continue
                break

        # check if the brick can fall down and to what z coordinate
        z_below = max(below_bricks.keys()) if below_bricks else 0
        z_delta = z_below + 1 - this[STA][Z]
        if z_delta < 0:
            # let the brick fall down to its lowest support (in-place)
            a_new = (this[STA][X], this[STA][Y], this[STA][Z] + z_delta)
            b_new = (this[END][X], this[END][Y], this[END][Z] + z_delta)
            bricks[i] = (a_new, b_new)

        # remember what other bricks are supporting this brick (bi-directional)
        if below_bricks:
            is_supported_by[i].update(below_bricks[z_below])
            for b in below_bricks[z_below]:
                does_support[b].add(i)

    return is_supported_by, does_support


def essential_brick_indexes(is_supported_by):
    # bricks that are only supporting one brick above them
    return {next(iter(v)) for v in is_supported_by.values() if len(v) == 1}


def num_supported_bricks(base_index, is_supported_by, does_support):
    removed_bricks = {base_index}  # the bricks that will fall down
    queue = [base_index]

    while queue:
        brick = queue.pop()
        for other in does_support[brick]:
            # is the other brick not supported by any other brick anymore?
            if not is_supported_by[other] - removed_bricks:
                # then it will fall down as well; queue the bricks it supported
                if other not in removed_bricks:
                    queue.append(other)
                    removed_bricks.add(other)

    # don't count the base brick itself
    return len(removed_bricks) - 1


def load(data):
    bricks = []
    for line in data.split("\n"):
        ax, ay, az, bx, by, bz = parse("{:d},{:d},{:d}~{:d},{:d},{:d}", line)
        assert ax <= bx and ay <= by and az <= bz
        bricks.append(((ax, ay, az), (bx, by, bz)))

    return bricks


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=22)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 443
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 69915
    puzzle.answer_b = ans2
