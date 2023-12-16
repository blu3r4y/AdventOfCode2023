# Advent of Code 2023

My solutions for the [AoC 2023](https://adventofcode.com/2023) challenges, written in Python.

🎄 🎄 🎄

## Puzzles

| Day | 🧩 Puzzle                                                                  | 🐍 Solution              | ⏳ Duration A | ⏳ Duration B |
| --: | :------------------------------------------------------------------------- | :----------------------- | ------------: | ------------: |
|   1 | **[Trebuchet?!](https://adventofcode.com/2023/day/1)**                     | [day1.py](src/day1.py)   |             - |             - |
|   2 | **[Cube Conundrum](https://adventofcode.com/2023/day/2)**                  | [day2.py](src/day2.py)   |             - |             - |
|   3 | **[Gear Ratios](https://adventofcode.com/2023/day/3)**                     | [day3.py](src/day3.py)   |             - |             - |
|   4 | **[Scratchcards](https://adventofcode.com/2023/day/4)**                    | [day4.py](src/day4.py)   |             - |             - |
|   5 | **[If You Give A Seed A Fertilizer](https://adventofcode.com/2023/day/5)** | [day5.py](src/day5.py)   |             - |             - |
|   6 | **[Wait For It](https://adventofcode.com/2023/day/6)**                     | [day6.py](src/day6.py)   |             - |             - |
|   7 | **[Camel Cards](https://adventofcode.com/2023/day/7)**                     | [day7.py](src/day7.py)   |         26 ms |         46 ms |
|   8 | **[Haunted Wasteland](https://adventofcode.com/2023/day/8)**               | [day8.py](src/day8.py)   |             - |        191 ms |
|   9 | **[Mirage Maintenance](https://adventofcode.com/2023/day/9)**              | [day9.py](src/day9.py)   |             - |             - |
|  10 | **[Pipe Maze](https://adventofcode.com/2023/day/10)**                      | [day10.py](src/day10.py) |        286 ms |        391 ms |
|  11 | **[Cosmic Expansion](https://adventofcode.com/2023/day/11)**               | [day11.py](src/day11.py) |         13 ms |         17 ms |
|  12 | **[Hot Springs](https://adventofcode.com/2023/day/12)**                    | [day12.py](src/day12.py) |         37 ms |      1,044 ms |
|  13 | **[Point of Incidence](https://adventofcode.com/2023/day/13)**             | [day13.py](src/day13.py) |         11 ms |         11 ms |
|  14 | **[Parabolic Reflector Dish](https://adventofcode.com/2023/day/14)**       | [day14.py](src/day14.py) |             - |      2.310 ms |
|  15 | **[Lens Library](https://adventofcode.com/2023/day/15)**                   | [day15.py](src/day15.py) |             - |             - |
|  16 | **[The Floor Will Be Lava](https://adventofcode.com/2023/day/16)**         | [day16.py](src/day16.py) |         12 ms |      3.409 ms |

Timings are measured on my computer in a non-scientific way.
Empty durations indicate a runtime of less than ten milliseconds.

## Requirements

### Python 3.12

Package requirements are specified in the **[requirements.txt](requirements.txt)** file.

```sh
pip install -r requirements.txt
```

You should install the pre-commit hooks and its dependencies to format the code before committing.

```sh
pip install pre-commit black isort flake8
pre-commit install
```
