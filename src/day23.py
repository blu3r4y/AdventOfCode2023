# Advent of Code 2023, Day 23
# (c) blu3r4y

import networkx as nx
from aocd.models import Puzzle
from funcy import print_calls, print_durations

PATH, FOREST, UP, RIGHT, DOWN, LEFT = ".", "#", "^", ">", "v", "<"
SLOPES = {UP: (0, -1), RIGHT: (1, 0), DOWN: (0, 1), LEFT: (-1, 0)}
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


@print_calls
@print_durations(unit="ms")
def part1(data):
    return solve(data, with_slopes=True)


@print_calls
@print_durations(unit="ms")
def part2(data):
    return solve(data, with_slopes=False)


def solve(data, with_slopes):
    grid, xmax, ymax = data
    start, end = (1, 0), (xmax - 1, ymax)

    G = parse_graph(grid, with_slopes)
    G = compress_graph(G)
    return longest_path_length(G, start, end)


def parse_graph(grid, with_slopes):
    G = nx.DiGraph()
    for xy in grid:
        if grid[xy] == FOREST:
            continue
        for succ in successors(grid, xy, with_slopes):
            G.add_edge(xy, succ)

    return G


def compress_graph(G):
    fringe = list(G.nodes)
    while fringe:
        node = fringe.pop()

        pre = set(G.predecessors(node))
        succ = set(G.successors(node))

        # compress nodes with the same neighbors in and out
        if len(pre) == 2 and pre == succ:
            a, b = pre

            ab_weight = G[a][node].get("weight", 1) + G[node][b].get("weight", 1)
            ba_weight = G[b][node].get("weight", 1) + G[node][a].get("weight", 1)

            G.add_edge(a, b, weight=ab_weight)
            G.add_edge(b, a, weight=ba_weight)
            G.remove_node(node)

    return G


def longest_path_length(graph, start, end):
    longest_path = 0
    for edges in nx.all_simple_edge_paths(graph, start, end):
        path_weight = sum(graph[u][v].get("weight", 1) for u, v in edges)
        longest_path = max(path_weight, longest_path)

    return longest_path


def successors(grid, xy, with_slopes):
    x, y = xy
    dxy = [SLOPES[grid[xy]]] if with_slopes and grid[xy] in SLOPES else DIRECTIONS
    for dx, dy in dxy:
        nxy = x + dx, y + dy
        if nxy in grid and grid[nxy] != FOREST:
            yield nxy


def load(data):
    grid = {}
    xmax, ymax = 0, 0
    for y, row in enumerate(data.split("\n")):
        ymax = max(ymax, y)
        for x, cell in enumerate(row):
            grid[(x, y)] = cell
            xmax = max(xmax, x)

    return grid, xmax, ymax


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=23)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 2190
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 6258
    puzzle.answer_b = ans2
