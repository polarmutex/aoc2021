from __future__ import annotations

import argparse
import os.path
import collections
from collections import Counter
from typing import List, Tuple, Generator, Set, Dict, NamedTuple
import heapq
from copy import deepcopy

from support import timing

INPUT_GITHUB = os.path.join("data", "2021", "day23_github.txt")
INPUT_GOOGLE = os.path.join("data", "2021", "day23_google.txt")
INPUT_REDDIT = os.path.join("data", "2021", "day23_reddit.txt")
INPUT_TWITTER = os.path.join("data", "2021", "day23_twitter.txt")
INPUT_S = """\
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

PolymerTemplate = str
Point = Tuple[int, int]

POS = {'A': 0, 'B': 1, 'C': 2, 'D': 3}


def parse(input: str):
    map = []
    for index, line in enumerate(input.splitlines()):
        map.append(line)
    return map


def solve(puzzle_input: str):
    solution1 = part1(puzzle_input)
    solution2 = part2(puzzle_input)
    return solution1, solution2


class State(NamedTuple):
    top: dict[int, int | None]
    row1: dict[int, int | None]
    row2: dict[int, int | None]
    row3: dict[int, int | None]
    row4: dict[int, int | None]

    def __hash__(self) -> int:
        return hash((
            tuple(self.top.items()),
            tuple(self.row1.items()),
            tuple(self.row2.items()),
            tuple(self.row3.items()),
            tuple(self.row4.items()),
        ))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        else:
            return id(self) < id(other)

    @property
    def completed(self) -> bool:
        return (
            all(k == v for k, v in self.row1.items()) and
            all(k == v for k, v in self.row2.items()) and
            all(k == v for k, v in self.row3.items()) and
            all(k == v for k, v in self.row4.items())
        )

    @classmethod
    def parse(cls, s: str, is_part_two: bool) -> State:
        lines = s.splitlines()
        if is_part_two:
            return cls(
                dict.fromkeys((0, 1, 3, 5, 7, 9, 10), None),
                {
                    0: POS[lines[2][3]],
                    1: POS[lines[2][5]],
                    2: POS[lines[2][7]],
                    3: POS[lines[2][9]],
                },
                {0: POS['D'], 1: POS['C'], 2: POS['B'], 3: POS['A']},
                {0: POS['D'], 1: POS['B'], 2: POS['A'], 3: POS['C']},
                {
                    0: POS[lines[3][3]],
                    1: POS[lines[3][5]],
                    2: POS[lines[3][7]],
                    3: POS[lines[3][9]],
                },
            )
        else:
            return cls(
                dict.fromkeys((0, 1, 3, 5, 7, 9, 10), None),
                {
                    0: POS[lines[2][3]],
                    1: POS[lines[2][5]],
                    2: POS[lines[2][7]],
                    3: POS[lines[2][9]],
                },
                {
                    0: POS[lines[3][3]],
                    1: POS[lines[3][5]],
                    2: POS[lines[3][7]],
                    3: POS[lines[3][9]],
                },
                {
                    0: POS['A'],
                    1: POS['B'],
                    2: POS['C'],
                    3: POS['D']
                },
                {
                    0: POS['A'],
                    1: POS['B'],
                    2: POS['C'],
                    3: POS['D']},
            )

    def __repr__(self) -> str:
        return (
            f'State(\n'
            f'    top={self.top!r},\n'
            f'    row1={self.row1!r},\n'
            f'    row2={self.row2!r},\n'
            f'    row3={self.row3!r},\n'
            f'    row4={self.row4!r},\n'
            f')'
        )


def next_states(
        score: int,
        state: State,
) -> Generator[tuple[int, State], None, None]:
    for k, v in state.top.items():
        if v is None:
            continue

        target_col = 2 + v * 2
        max_c = max(target_col, k)
        min_c = min(target_col, k)
        to_move_top = max_c - min_c

        if all(
            k2 <= min_c or k2 >= max_c or v2 is None
            for k2, v2 in state.top.items()
        ):
            if state.row4[v] is None:
                yield (
                    score + (to_move_top + 4) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row4={**state.row4, v: v},
                    )
                )
            elif state.row4[v] == v and state.row3[v] is None:
                yield (
                    score + (to_move_top + 3) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row3={**state.row3, v: v},
                    ),
                )
            elif (
                    state.row4[v] == v and
                    state.row3[v] == v and
                    state.row2[v] is None
            ):
                yield (
                    score + (to_move_top + 2) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row2={**state.row2, v: v},
                    ),
                )
            elif (
                    state.row4[v] == v and
                    state.row3[v] == v and
                    state.row2[v] == v and
                    state.row1[v] is None
            ):
                yield (
                    score + (to_move_top + 1) * 10 ** v,
                    state._replace(
                        top={**state.top, k: None},
                        row1={**state.row1, v: v},
                    ),
                )

    potential_targets = {k for k, v in state.top.items() if v is None}
    for i in range(4):
        row1_val = state.row1[i]
        row2_val = state.row2[i]
        row3_val = state.row3[i]
        row4_val = state.row4[i]
        # this row is done! do not move!
        if row1_val == row2_val == row3_val == row4_val == i:
            continue

        for target in potential_targets:
            src_col = 2 + i * 2
            max_c = max(src_col, target)
            min_c = min(src_col, target)
            to_move_top = max_c - min_c

            if all(
                k2 <= min_c or k2 >= max_c or v2 is None
                for k2, v2 in state.top.items()
            ):
                if (
                        row1_val is not None and (
                            row1_val != i or
                            row2_val != i or
                            row3_val != i or
                            row4_val != i
                        )
                ):
                    yield (
                        score + (to_move_top + 1) * 10 ** row1_val,
                        state._replace(
                            top={**state.top, target: row1_val},
                            row1={**state.row1, i: None},
                        )
                    )
                elif (
                        row1_val is None and
                        row2_val is not None and (
                            row2_val != i or
                            row3_val != i or
                            row4_val != i
                        )
                ):
                    yield (
                        score + (to_move_top + 2) * 10 ** row2_val,
                        state._replace(
                            top={**state.top, target: row2_val},
                            row2={**state.row2, i: None},
                        )
                    )
                elif (
                        row1_val is None and
                        row2_val is None and
                        row3_val is not None and (
                            row3_val != i or
                            row4_val != i
                        )
                ):
                    yield (
                        score + (to_move_top + 3) * 10 ** row3_val,
                        state._replace(
                            top={**state.top, target: row3_val},
                            row3={**state.row3, i: None},
                        )
                    )
                elif (
                        row1_val is None and
                        row2_val is None and
                        row3_val is None and
                        row4_val is not None and
                        row4_val != i
                ):
                    yield (
                        score + (to_move_top + 4) * 10 ** row4_val,
                        state._replace(
                            top={**state.top, target: row4_val},
                            row4={**state.row4, i: None},
                        )
                    )


def compute(s: str, is_part_two: bool) -> int:
    initial = State.parse(s, is_part_two)

    seen = set()
    todo = [(0, initial)]
    while todo:
        score, state = heapq.heappop(todo)

        if state.completed:
            return score
        elif state in seen:
            continue
        else:
            seen.add(state)

        for tp in next_states(score, state):
            heapq.heappush(todo, tp)

    raise AssertionError('unreachable')


def part1(input: str) -> int:
    return compute(input, False)


def part2(input: str) -> int:
    return compute(input, True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_GITHUB)
    args = parser.parse_args()

    # with open(args.data_file) as f, timing():
    #   solutions = solve(f.read())
    #    print("\n".join(str(solution) for solution in solutions))
    solutions = solve(INPUT_S)
    print("\n".join(str(solution) for solution in solutions))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
