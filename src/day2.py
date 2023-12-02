# Advent of Code 2023, Day 2
# (c) blu3r4y

from functools import reduce
from operator import mul

from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(games):
    maxbag = {"red": 12, "green": 13, "blue": 14}
    result = 0

    for no, game in enumerate(games, 1):
        game_possible = True
        for cubeset in game:
            thisbag = maxbag.copy()
            for color, count in cubeset.items():
                thisbag[color] -= count

            possible = all(v >= 0 for v in thisbag.values())
            game_possible &= possible

        result += no if game_possible else 0

    return result


@print_calls
@print_durations(unit="ms")
def part2(games):
    result = 0
    for game in games:
        minbag = {}
        for cubeset in game:
            for color, count in cubeset.items():
                minbag[color] = max(minbag.get(color, 0), count)

        power = reduce(mul, minbag.values())
        result += power

    return result


@collecting
def load(data):
    for line in data.split("\n"):
        _, game = parse("Game {:d}: {}", line).fixed

        gameset = []
        for cubeset in game.split(";"):
            cubeset = [s.strip() for s in cubeset.split(",")]
            cubeset = [parse("{:d} {}", s).fixed[::-1] for s in cubeset]
            gameset.append(dict(cubeset))

        yield gameset


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=2)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 2169
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 60948
    puzzle.answer_b = ans2
