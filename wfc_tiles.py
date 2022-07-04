from dataclasses import dataclass
import enum


class Grid:
    def __init__(self) -> None:
        return

    def reset(self):
        return

    def setTile(self, x: int, y: int):
        return


RULE_COUNT = 5


class Rule(enum):
    Blank = 0,
    Left = 1,
    Up = 2,
    Right = 3,
    Down = 4,


class Solver:
    def __init__(self) -> None:
        self.rules = []
        self.rules[Rule.Blank] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Left] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Blank] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Blank] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Blank] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
