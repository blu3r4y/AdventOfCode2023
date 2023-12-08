# Advent of Code 2023, Day 5
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import chunks, lmap, print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(maps):
    seeds, stages = maps

    # apply all stages to all seeds and
    # find the smallest resulting location
    smallest = None
    for seed in seeds:
        for stage in stages:
            seed = map_seed(seed, stage)

        smallest = min(smallest or seed, seed)

    return smallest


@print_calls
@print_durations(unit="ms")
def part2(maps):
    seeds, stages = maps

    # apply all stages to each seed range, where,
    # for each seed range, we collect all possible resulting ranges,
    # and then find the smallest resulting location across all ranges
    smallest = None
    for x, xsize in chunks(2, seeds):
        ranges = [(x, xsize)]
        for stage in stages:
            mapped_ranges = []
            for y, ysize in ranges:
                mapped_ranges.extend(map_range(y, ysize, stage))
            ranges = mapped_ranges

        # find the smallest location across all ranges
        location = min(ranges, key=lambda x: x[0])[0]
        smallest = min(smallest or location, location)

    return smallest


def map_seed(x, mapping):
    for dst, src, size in mapping:
        if src <= x < src + size:
            return x - src + dst
    return x


def map_range(x, xsize, mapping):
    if not mapping:  # recursion anchor
        return [(x, xsize)]

    # we split intervals left to right, so sort by src ascending
    mapping = sorted(mapping, key=lambda x: x[1])

    # get the first mapping that overlaps with the base range
    dst, src, msize = mapping.pop(0)
    while not range_overlap(x, xsize, src, msize):
        if not mapping:
            return [(x, xsize)]
        dst, src, msize = mapping.pop(0)

    # clip this mapping to [x, x + xsize]
    clipsrc = min(max(src, x), x + xsize - 1)
    clipmsize = min(msize - clipsrc + src, x + xsize - clipsrc)

    # the mapping is contained within the base range,
    # so we can always split this into three intervals
    a, asize = x, clipsrc - x
    b, bsize = clipsrc, clipmsize
    x, xsize = clipsrc + clipmsize, x + xsize - clipsrc - clipmsize

    result = []

    if asize > 0:
        result.extend(map_range(a, asize, mapping.copy()))
    if bsize > 0:
        # the middle interval is the only one that is actually mapped
        # and since mappings never overlap, we do not need to recurse
        offset = dst - src
        result.append((b + offset, bsize))
    if xsize > 0:
        result.extend(map_range(x, xsize, mapping.copy()))

    return result


def range_overlap(a, asize, b, bsize):
    return not (a + asize <= b or b + bsize <= a)


def load(data):
    blocks = data.split("\n\n")
    seeds = lmap(int, parse("seeds: {}", blocks[0]).fixed[0].split())

    stages = []
    for block in blocks[1:]:
        blocklines = block.splitlines()[1:]
        stage = [tuple(map(int, line.split())) for line in blocklines]
        stages.append(stage)

    return seeds, stages


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=5)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 3374647
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6082852
    puzzle.answer_b = ans2
