# Advent of Code 2023, Day 17
# (c) blu3r4y

from collections import namedtuple
from queue import PriorityQueue

from aocd.models import Puzzle
from funcy import print_calls, print_durations

# current position, orientation, and number of steps steps taken
State = namedtuple("State", ["pos", "orient", "steps"])


@print_calls
@print_durations(unit="ms")
def part1(data):
    heatmap, goal = data
    return solve(heatmap, start=0, goal=goal, smin=0, smax=3)


@print_calls
@print_durations(unit="ms")
def part2(data):
    heatmap, goal = data
    return solve(heatmap, start=0, goal=goal, smin=4, smax=10)


def solve(heatmap, start, goal, smin, smax):
    starts = [  # start moving right or down
        State(pos=start, orient=1, steps=0),
        State(pos=start, orient=1j, steps=0),
    ]

    return astar_search(heatmap, starts, goal, goal, smin, smax)


def astar_search(heatmap, starts, goal, limit, smin, smax):
    closed = {start: 0 for start in starts}
    openpq = PriorityQueue()
    tiebreaker = 0
    for start in starts:
        openpq.put((0, tiebreaker, start))
        tiebreaker += 1

    while not openpq.empty():
        total_heat, _, current = openpq.get()
        if current.pos == goal and current.steps >= smin:
            return total_heat

        for succ in successor_states(current, limit, smin, smax):
            new_heat = closed[current] + heatmap[succ.pos]
            if succ not in closed or new_heat < closed[succ]:
                closed[succ] = new_heat
                estimate = new_heat + remaining_manhattan_heat(succ, goal)
                openpq.put((estimate, tiebreaker, succ))
                tiebreaker += 1


def successor_states(state, limit, smin, smax):
    # go steps if we haven't been going steps for too long
    if state.steps < smax:
        nxt = state.pos + state.orient
        if within_grid_limits(nxt, limit):
            yield State(pos=nxt, orient=state.orient, steps=state.steps + 1)

    # turn right or left
    if smin <= state.steps <= smax:
        for turn in (1j, -1j):
            nxt = state.pos + (state.orient * turn)
            if within_grid_limits(nxt, limit):
                yield State(pos=nxt, orient=state.orient * turn, steps=1)


def within_grid_limits(pos, bounds):
    return 0 <= pos.real <= bounds.real and 0 <= pos.imag <= bounds.imag


def remaining_manhattan_heat(state, goal) -> int:
    a, b = goal, state.pos
    return int(abs(a.imag - b.imag) + abs(a.real - b.real))


def load(data):
    heatmap = {}
    lines = data.splitlines()
    ncols, nrows = len(lines[0]), len(lines)
    for y, line in enumerate(lines):
        for x, heat in enumerate(line):
            heatmap[x + y * 1j] = int(heat)

    goal = ncols - 1 + (nrows - 1) * 1j
    return heatmap, goal


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=17)

    ans1 = part1(load(puzzle.input_data))
    assert ans1 == 755
    puzzle.answer_a = ans1

    ans2 = part2(load(puzzle.input_data))
    assert ans2 == 881
    puzzle.answer_b = ans2
