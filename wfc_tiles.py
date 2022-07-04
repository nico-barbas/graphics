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


class Entropy_Tile:
    def __init__(self) -> None:
        self.entropy_count = 5
        self.open_set = [True for i in range(5)]
        self.value = -1


class Solver:
    def __init__(self, width: int, height: int) -> None:
        self.rules = []
        self.rules[Rule.Blank] = [
            [True, True, False, False, False],
            [True, False, True, False, False],
            [True, False, False, True, False],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Left] = [
            [False, False, True, True, True],
            [False, True, False, True, True],
            [True, False, False, True, False],
            [False, True, True, True, False],
        ]
        self.rules[Rule.Up] = [
            [False, False, True, True, True],
            [False, True, False, True, True],
            [False, True, True, False, True],
            [True, False, False, False, True],
        ]
        self.rules[Rule.Right] = [
            [True, True, False, False, False],
            [False, True, False, True, True],
            [False, True, True, False, True],
            [False, True, True, True, False],
        ]
        self.rules[Rule.Down] = [
            [False, False, True, True, True],
            [True, False, True, False, False],
            [False, True, True, False, True],
            [False, True, True, True, False],
        ]

        self.width = width
        self.height = height
        self.tiles = [Entropy_Tile() for i in range(width*height)]

    def solve(self):
        pass

    def collapse(self):
        def get_left(self, x: int, y: int) -> Entropy_Tile:
            if x > 0:
                return self.tiles[y*self.width + x-1]
            else:
                return None

        def get_right(self, x: int, y: int) -> Entropy_Tile:
            if x < self.width - 1:
                return self.tiles[y*self.width + x+1]
            else:
                return None

        def get_up(self, x: int, y: int) -> Entropy_Tile:
            if y > 0:
                return self.tiles[(y-1)*self.width + x]
            else:
                return None

        def get_left(self, x: int, y: int) -> Entropy_Tile:
            if y > self.height-1:
                return self.tiles[(y+1)*self.width + x]
            else:
                return None

        for y in range(self.height):
            for x in range(self.width):
                pass
