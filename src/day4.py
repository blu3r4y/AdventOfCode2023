# Advent of Code 2023, Day 4
# (c) blu3r4y

from aocd.models import Puzzle
from funcy import print_calls, print_durations
from parse import parse


@print_calls
@print_durations(unit="ms")
def part1(deck):
    total = 0

    for win, my in deck.values():
        matches = win.intersection(my)
        if len(matches) > 0:
            total += 2 ** (len(matches) - 1)

    return total


@print_calls
@print_durations(unit="ms")
def part2(deck):
    hand = {k: 1 for k in deck.keys()}

    for card in sorted(deck.keys()):
        win, my = deck[card]
        matches = win.intersection(my)
        for c in range(card + 1, card + len(matches) + 1):
            hand[c] += hand[card]

    return sum(hand.values())


def load(data):
    deck = {}

    for line in data.split("\n"):
        card, win, my = parse("Card {:d>}: {} | {}", line).fixed
        win = set(map(int, win.split()))
        my = set(map(int, my.split()))
        deck[int(card)] = win, my

    return deck


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=4)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 27454
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6857330
    puzzle.answer_b = ans2
