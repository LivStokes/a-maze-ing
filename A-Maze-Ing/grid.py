from __future__ import annotations
from dataclasses import dataclass
from hex_helpers import Direction, HexDigit, is_wall, hex_break, hex_build, hex_flip
from collections.abc import Iterator, Callable
from typing import Self

@dataclass(frozen=True)
class Cell:
    row: int
    col: int

    def __add__(self, vector: tuple[int, int]) -> Cell:
        return Cell(self.row + vector[0], self.col + vector[1])
    
    def __str__(self) -> str:
        return f"{self.row},{self.col}"

    def neighbour(self, dir: Direction) -> Cell:
        return self + dir.uni_vector

    def __post_init__(self):
        if type(self.row) is not int:
            raise TypeError(f"row must be int not {type(self.row)}")
        if type(self.col) is not int:
            raise TypeError("col must be int")



class Grid[T]:
    def __init__(self, size: tuple[int, int], initial_val: T):
        self.height, self.width = size
        self._data: list[list[T]]
        self._data = [[initial_val] * self.width for _ in range(self.height)]

    def __getitem__(self, cell: Cell) -> T:
        self._invalid_cell(cell)
        return self._data[cell.row][cell.col]

    def __setitem__(self, cell: Cell, value: T) -> None:
        self._invalid_cell(cell)
        self._data[cell.row][cell.col] = value

    def __contains__(self, cell: Cell) -> bool:
        return (cell.row >= 0 and cell.row < self.height and
                cell.col >= 0 and cell.col < self.width)

    def __iter__(self) -> Iterator[Cell]:
        for row in range(self.height):
            for col in range(self.width):
                yield Cell(row, col)
    
    def _is_endrow(self, cell: Cell) -> bool:
        return cell.col == self.width - 1

    def _invalid_cell(self, cell: Cell) -> None:
        if cell not in self:
            raise IndexError("Invalid Cell")

class HexGrid(Grid[HexDigit]):
    def __init__(self, size: tuple[int, int], initial_val: HexDigit = 15):
        super().__init__(size, initial_val)

    def __str__(self) -> str:
        string: str = ""
        for row in self._data:
            for cell in row:
                string += format(cell, "X")
            string += "\n"
        return string


class BoolGrid(Grid[bool]):
    def __str__(self) -> str:
        parts: list[str] = []
        for row in self._data:
            for pixel in row:
                parts.append("██" if pixel else "  ")
            parts.append("\n")
        return "".join(parts)
    
class Maze(HexGrid):
    def __init__(self, size: tuple[int, int], entry: Cell, exit: Cell):
        super().__init__(size)
        self.entry = entry
        self.exit = exit

    def is_coherent(self) -> bool:
        for row in range(self.height - 1):
            for col in range(self.width - 1):
                for dir in (Direction.E, Direction.S):
                    cell = Cell(row, col)
                    wall1 = is_wall(self[cell], dir)
                    wall2 = is_wall(self[cell.neighbour(dir)], dir.opposite)
                    if wall1 != wall2:
                        return False
        return True

    @property
    def is_small(self) -> bool:
        return self.height < 7 or self.width < 9

    def is_wall(self, cell: Cell, direction: Direction) -> bool:
        return is_wall(self[cell], direction)
    
    def is_closed(self, cell: Cell) -> bool:
        return self[cell] == 15

    def _action_wall(self, cell: Cell, dir: Direction,
                     action: Callable[[HexDigit, HexDigit, Direction],
                                      tuple[HexDigit, HexDigit]]) -> None:
        cell2 = cell.neighbour(dir)
        hex1 = self[cell]
        hex2 = self[cell2]
        hex1, hex2 = action(hex1, hex2, dir)
        self[cell] = hex1
        self[cell2] = hex2

    def break_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_break)

    def build_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_build)

    def flip_wall(self, cell: Cell, dir: Direction) -> None:
        self._action_wall(cell, dir, hex_flip)

