from grid import Cell, HexGrid
from hex_helpers import HexDigit, hex_break, Direction, hex_build, hex_flip
from typing import Callable
from random import sample, random, choice, seed
from contextlib import suppress

# seed(1)


class Maze:
    def __init__(self, size: tuple[int, int],
                 entry_exit: tuple[Cell, Cell] | None = None,
                 ft: bool = True):
        self.height, self.width = size
        self.grid: HexGrid = HexGrid(size, 15)
        if entry_exit is None:
            self.entry = Cell(0, 0)
            self.exit = Cell(self.height -1, self.width -1)
        else:
            self.entry, self.exit = entry_exit
        self.forty_two: list[Cell] = self._forty_two(ft)
        if not self._entry_exit_validity():
            raise ValueError("Invalid entry/exit")


    def _forty_two(self, ft) -> list[Cell]:
        if self.height < 7 or self.width < 9 or not ft:
            return []
        middle_cell = Cell(self.height // 2, self.width // 2)
        forty_two_vectors = [(0, -1), (0, -2), (0, -3), (-1, -3), (-2, -3),
                             (1, -1), (2, -1), (0, 1), (0, 2), (0, 3), (1, 1),
                             (2, 1), (2, 2), (2, 3), (-1, 3), (-2, 3), (-2, 2),
                             (-2, 1)]
        return [middle_cell + vector for vector in forty_two_vectors]

    def _entry_exit_validity(self) -> bool:
        return (self.entry not in self.forty_two and
                self.exit not in self.forty_two and
                self.entry in self.grid and self.exit in self.grid and
                self.entry != self.exit)

    def _action_wall(self, cell: Cell, dir: Direction,
                     action: Callable[[HexDigit, HexDigit, Direction],
                                      tuple[HexDigit, HexDigit]]) -> None:
        cell2 = cell.neighbour(dir)
        hex1 = self.grid[cell]
        hex2 = self.grid[cell2]
        hex1, hex2 = action(hex1, hex2, dir)
        self.grid[cell] = hex1
        self.grid[cell2] = hex2

    def break_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_break)

    def build_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_build)

    def flip_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_flip)

    def _hasnt_been_visited(self, cell: Cell) -> bool:
        return self.grid[cell] == 15

    def imperfect(self, likelyhood: float = 0.1) -> None:
        for cell in self.grid:
            if cell not in self.forty_two and random() < likelyhood:
                direction = choice(list(Direction))
                if (cell.neighbour(direction) not in self.forty_two and
                    cell.neighbour(direction) in self.grid):
                    self.break_wall(cell, direction)


    def backtracking(self, cell: Cell = Cell(0, 0)):
        for dir in sample(list(Direction), k=len(Direction)):
            with suppress(IndexError):
                if (self._hasnt_been_visited(cell.neighbour(dir)) and
                 cell.neighbour(dir) not in self.forty_two):
                    self.break_wall(cell, dir)
                    self.backtracking(cell.neighbour(dir))

