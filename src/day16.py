# Advent of Code 2023, Day 16
# (c) blu3r4y

from itertools import chain

from aocd.models import Puzzle
from funcy import print_calls, print_durations

EMPTY, MIRROR_RL, MIRROR_LR, SPLITTER_V, SPLITTER_H = ".", "/", "\\", "|", "-"


@print_calls
@print_durations(unit="ms")
def part1(data):
    grid, xmax, ymax = data
    return number_of_energized_tiles(grid, xmax, ymax, 0, 1)


@print_calls
@print_durations(unit="ms")
def part2(data):
    grid, xmax, ymax = data

    edge = chain(
        ((x, 1j) for x in range(xmax + 1)),
        ((x + ymax * 1j, -1j) for x in range(xmax + 1)),
        ((y * 1j, 1) for y in range(ymax + 1)),
        ((xmax + y * 1j, -1) for y in range(ymax + 1)),
    )

    max_energy = 0
    for start, direction in edge:
        energy = number_of_energized_tiles(grid, xmax, ymax, start, direction)
        max_energy = max(max_energy, energy)

    return max_energy


def number_of_energized_tiles(grid, xmax, ymax, start, direction):
    beams = [(start, direction)]
    touched = {start}
    beamcache = set()

    while beams:
        pos, orient = beams.pop()

        # keep going until we hit the edge
        while 0 <= pos.real <= xmax and 0 <= pos.imag <= ymax:
            if (pos, orient) in beamcache:
                break  # already visited

            beamcache.add((pos, orient))
            touched.add(pos)

            # continue if we hit empty space
            symbol = grid.get(pos)
            if not symbol:
                pass

            # change orientation if we hit a mirror
            elif symbol == MIRROR_RL:
                orient *= 1j if orient.imag else -1j
            elif symbol == MIRROR_LR:
                orient *= -1j if orient.imag else 1j

            # split the beam if we hit a splitter
            elif symbol == SPLITTER_V and not orient.imag:
                beams.append((pos, orient * 1j))
                beams.append((pos, orient * -1j))
                break
            elif symbol == SPLITTER_H and not orient.real:
                beams.append((pos, orient * 1j))
                beams.append((pos, orient * -1j))
                break

            pos += orient

    return len(touched)


def load(data):
    grid, xmax, ymax = {}, 0, 0
    for y, line in enumerate(data.split("\n")):
        ymax = max(ymax, y)
        for x, char in enumerate(line):
            xmax = max(xmax, x)
            if char != EMPTY:
                grid[x + y * 1j] = char

    return grid, xmax, ymax


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=16)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 8389
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 8564
    puzzle.answer_b = ans2
