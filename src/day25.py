# Advent of Code 2023, Day 25
# (c) blu3r4y

import networkx as nx
from aocd.models import Puzzle
from funcy import print_calls, print_durations


@print_calls
@print_durations(unit="ms")
def part1(G):
    # find the minimum edge cut and remove those edges
    cutset = nx.minimum_edge_cut(G)
    G.remove_edges_from(cutset)

    # multiple the sizes of the two connected components
    a, b = list(nx.connected_components(G))
    return len(a) * len(b)


def load(data):
    G = nx.Graph()
    for line in data.split("\n"):
        src, dst = line.split(": ")
        G.add_edges_from((src, d) for d in dst.split())

    return G


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=25)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 538560
    puzzle.answer_a = ans1
