# Advent of Code 2023, Day 10
# (c) blu3r4y

import networkx as nx
from aocd.models import Puzzle
from funcy import pairwise, print_calls, print_durations

ALL_NEIGHBORS = ((0, 1), (1, 0), (0, -1), (-1, 0))
PIPE_NEIGHBORS = {
    "|": ((0, -1), (0, 1)),
    "-": ((-1, 0), (1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((0, 1), (-1, 0)),
    "F": ((0, 1), (1, 0)),
    ".": (),
    "S": (),
}


@print_calls
@print_durations(unit="ms")
def part1(cells):
    G, start = build_graph(cells)

    # find longest path from start to any other point,
    # but only consider the subgraph that is reachable from start
    loop = nx.node_connected_component(G, start)
    return nx.eccentricity(G.subgraph(loop), start)


@print_calls
@print_durations(unit="ms")
def part2(cells):
    G, start = build_graph(cells)

    # find (any) loop that is reachable from the start
    cycle = [u for u, v in nx.find_cycle(G, start)]

    # compute the polygon area and derive the number of inner grid points
    area = compute_positive_polygon_area(cycle)
    return compute_points_inside_polygon(area, len(cycle))


def build_graph(cells):
    G = nx.DiGraph()

    for x, y in cells:
        G.add_node((x, y))
        for px, py in neighbors(x, y, cells):
            G.add_node((px, py))
            G.add_edge((x, y), (px, py))

    # add missing out edges from start node
    start = next((pos for pos, v in cells.items() if v == "S"))
    for v1, v2 in G.in_edges(start):
        G.add_edge(v2, v1)

    return G.to_undirected(reciprocal=True), start


def neighbors(x, y, cells):
    for dx, dy in PIPE_NEIGHBORS[cells[(x, y)]]:
        px, py = x + dx, y + dy
        if (px, py) in cells:
            yield px, py


def compute_positive_polygon_area(vert):
    if (area := compute_polygon_area(vert)) >= 0:
        return area

    # if the vertices were not given in counter-clockwise order,
    # the result will be negative, so reverse and try again
    return compute_polygon_area(vert[::-1])


def compute_polygon_area(vert):
    area = 0

    # Triangle formula to compute area of a polygon
    # https://en.m.wikipedia.org/wiki/Shoelace_formula#Triangle_formula
    for (x1, y1), (x2, y2) in pairwise(vert + [vert[0]]):
        area += x1 * y2 - x2 * y1

    return area / 2


def compute_points_inside_polygon(area, num_edges):
    # Pick's theorem to compute the inner points of a grid-based polygon
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    return int(area - num_edges / 2 + 1)


def load(data):
    cells = {}
    for y, row in enumerate(data.split("\n")):
        for x, cell in enumerate(row):
            cells[(x, y)] = cell

    return cells


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=10)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 6828
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 459
    puzzle.answer_b = ans2
