# Advent of Code 2023, Day 7
# (c) blu3r4y

import functools
import itertools
from collections import Counter

from aocd.models import Puzzle
from funcy import collecting, print_calls, print_durations

# map card ranks to pure integers
RANKS_PART1 = "23456789TJQKA"
RANKS_PART2 = "J23456789TQKA"


@print_calls
@print_durations(unit="ms")
def part1(hands):
    hands = sorted(hands, key=functools.cmp_to_key(compare_hands))
    return total_winnings(bid for _, bid in hands)


@print_calls
@print_durations(unit="ms")
def part2(hands):
    hands = sorted(hands, key=functools.cmp_to_key(compare_hands_with_joker))
    return total_winnings(bid for _, bid in hands)


def compare_hands(h1, h2):
    c1, c2 = h1[0], h2[0]
    s1, s2 = hand_strength(c1), hand_strength(c2)

    if s1 > s2:
        return 1
    elif s1 < s2:
        return -1
    return compare_individual_cards(c1, c2)


def compare_hands_with_joker(h1, h2):
    c1, c2 = h1[0], h2[0]
    s1 = max(map(hand_strength, permute_joker(c1)))
    s2 = max(map(hand_strength, permute_joker(c2)))

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


def permute_joker(cards):
    # indices of all joker cards and all possible permutations
    indices = [i for i, card in enumerate(cards) if card == 0]
    ranks_without_joker = range(1, len(RANKS_PART2))
    for perm in itertools.product(ranks_without_joker, repeat=len(indices)):
        yield tuple(
            perm[indices.index(i)] if i in indices else original_card
            for i, original_card in enumerate(cards)
        )


def hand_strength(cards):
    vals = list(Counter(cards).values())

    if 5 in vals:  # five of a kind
        return 7
    elif 4 in vals:  # four of a kind
        return 6
    elif 2 in vals and 3 in vals:  # full house
        return 5
    elif 3 in vals and vals.count(1) == 2:  # three of a kind
        return 4
    elif vals.count(2) == 2 and vals.count(1) == 1:  # two pair
        return 3
    elif vals.count(2) == 1 and vals.count(1) == 3:  # one pair
        return 2
    elif vals.count(1) == 5:  # high card
        return 1


def total_winnings(bids):
    total = 0
    for rank, bid in enumerate(bids, 1):
        total += bid * (rank)
    return total


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
