# Advent of Code 2023, Day 7
# (c) blu3r4y

from functools import cmp_to_key, partial
from collections import Counter

from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations

# map card ranks to pure integers
RANKS_PART1 = "23456789TJQKA"
RANKS_PART2 = "J23456789TQKA"


@print_calls
@print_durations(unit="ms")
def part1(hands):
    return total_winnings(hands, cmp_func=hand_strength)


@print_calls
@print_durations(unit="ms")
def part2(hands):
    return total_winnings(hands, cmp_func=hand_strength_with_joker)


def total_winnings(hands, cmp_func):
    key_func = cmp_to_key(partial(compare_hands, cmp_func=cmp_func))
    hands = sorted(hands, key=key_func)

    winnings = 0
    for rank, (_, bid) in enumerate(hands, 1):
        winnings += bid * (rank)

    return winnings


def compare_hands(h1, h2, cmp_func):
    c1, c2 = h1[0], h2[0]
    s1, s2 = cmp_func(c1), cmp_func(c2)

    if s1 > s2:
        return 1
    elif s1 < s2:
        return -1

    return compare_individual_cards(c1, c2)


def compare_individual_cards(h1, h2):
    for c1, c2 in zip(h1, h2):
        if c1 > c2:
            return 1
        elif c1 < c2:
            return -1

    return 0


def hand_strength(cards):
    c = list(Counter(cards).values())

    if 5 in c:  # five of a kind
        return 7
    elif 4 in c:  # four of a kind
        return 6
    elif 3 in c and 2 in c:  # full house
        return 5
    elif 3 in c:  # three of a kind
        return 4
    elif c.count(2) == 2:  # two pair
        return 3
    elif c.count(2) == 1:  # one pair
        return 2

    return 1  # high card


def hand_strength_with_joker(cards):
    counts = Counter(cards)

    # sizes of unique card sets, excluding joker cards
    c = list(v for k, v in counts.items() if k != 0)
    j = counts[0]  # number of joker cards

    # five of a kind
    if (
        (5 in c)
        or (4 in c and j == 1)
        or (3 in c and j == 2)
        or (2 in c and j == 3)
        or (1 in c and j == 4)
        or (j == 5)
    ):
        return 7

    # four of a kind
    elif (
        (4 in c)
        or (3 in c and j == 1)
        or (2 in c and j == 2)
        or (1 in c and j == 3)
        or (j == 4)
    ):
        return 6

    # full house
    elif (3 in c and 2 in c) or (c.count(2) == 2 and j == 1):
        return 5

    # three of a kind
    elif (3 in c) or (2 in c and j == 1) or (1 in c and j == 2) or (j == 3):
        return 4

    # two pair
    elif (c.count(2) == 2) or (c.count(2) == 1 and j == 1):
        return 3

    # one pair
    elif (c.count(2) == 1) or (c.count(1) == 4 and j == 1):
        return 2

    # high card
    return 1


@collecting
def load(data, ranks):
    for line in data.split("\n"):
        cards, bid = line.split()
        yield tuple(ranks.index(c) for c in cards), int(bid)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=7)

    ans1 = part1(load(puzzle.input_data, RANKS_PART1))
    assert ans1 == 246424613
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data, RANKS_PART2))
    assert ans2 == 248256639
    puzzle.answer_b = ans2
