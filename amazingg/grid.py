from __future__ import annotations
from dataclasses import dataclass
from hex_helpers import Direction, HexDigit, validate_hex, is_wall
from collections.abc import Iterator

@dataclass(frozen=True)
class Cell:
    row: int
    col: int

    def __add__(self, vector: tuple[int, int]) -> Cell:
        return Cell(self.row + vector[0], self.col + vector[1])

    def neighbour(self, dir: Direction) -> Cell:
        return self + dir.uni_vector



class Grid:
    def __init__(self, size: tuple[int, int], initial_val: HexDigit = 15):
        self.height, self.width = size
        self._data: list[list[HexDigit]]
        self._data = [[initial_val] * self.width for _ in range(self.height)]

    def __getitem__(self, cell: Cell) -> HexDigit:
        self._invalid_cell(cell)
        return self._data[cell.row][cell.col]

    def __setitem__(self, cell: Cell, value: HexDigit) -> None:
        self._invalid_cell(cell)
        validate_hex(value)
        self._data[cell.row][cell.col] = value

    def __str__(self) -> str:
        string: str = ""
        for row in self._data:
            for cell in row:
                string += format(cell, "X")
            string += "\n"
        return string

    def __contains__(self, cell: Cell) -> bool:
        return (cell.row >= 0 and cell.row < self.height and
                cell.col >= 0 and cell.col < self.width)


    def __iter__(self) -> Iterator[Cell]:
        for row in range(self.height):
            for col in range(self.width):
                yield Cell(row, col)

    def _invalid_cell(self, cell: Cell) -> None:
        if not ((0 <= cell.row < self.height)
                and (0 <= cell.col < self.width)):
            raise IndexError("Invalid Cell")

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