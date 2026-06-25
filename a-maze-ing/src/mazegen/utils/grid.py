"""Module defining Cell, Grid, and Maze data structures for maze generation
and manipulation."""
from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Iterator, Callable
from .hex_helpers import (Direction, HexDigit, is_wall, hex_break, hex_build,
                          hex_flip)


@dataclass(frozen=True)
class Cell:
    """Immutable grid coordinate represented as a row and column pair."""
    row: int
    col: int

    def __add__(self, vector: tuple[int, int]) -> Cell:
        """Return a new Cell offset by the given (row, col) vector."""
        return Cell(self.row + vector[0], self.col + vector[1])

    def __str__(self) -> str:
        """Return the cell as a 'row,col' string."""
        return f"{self.row},{self.col}"

    def neighbour(self, dir: Direction) -> Cell:
        """Return the adjacent cell in the given direction."""
        return self + dir.uni_vector

    def __post_init__(self) -> None:
        """Validate that row and col are integers."""
        if type(self.row) is not int:
            raise TypeError(f"row must be int not {type(self.row)}")
        if type(self.col) is not int:
            raise TypeError("col must be int")


class Grid[T]:
    """Generic 2D grid supporting cell-based access, iteration, and bounds
    checking."""
    def __init__(self, size: tuple[int, int], initial_val: T) -> None:
        """Initialize the grid with the given dimensions and fill every cell
        with the initial value."""
        self.height, self.width = size
        self._data: list[list[T]]
        self._data = [[initial_val] * self.width for _ in range(self.height)]

    def __getitem__(self, cell: Cell) -> T:
        """Return the value at the given cell, raising IndexError if out of
        bounds."""
        self._invalid_cell(cell)
        return self._data[cell.row][cell.col]

    def __setitem__(self, cell: Cell, value: T) -> None:
        """Set the value at the given cell, raising IndexError if out of
        bounds."""
        self._invalid_cell(cell)
        self._data[cell.row][cell.col] = value

    def __contains__(self, cell: Cell) -> bool:
        """Return True if the cell lies within the grid bounds."""
        return (cell.row >= 0 and cell.row < self.height and
                cell.col >= 0 and cell.col < self.width)

    def __iter__(self) -> Iterator[Cell]:
        """Yield every cell in the grid in row-major order."""
        for row in range(self.height):
            for col in range(self.width):
                yield Cell(row, col)

    def _is_endrow(self, cell: Cell) -> bool:
        """Return True if the cell is in the last column of its row."""
        return cell.col == self.width - 1

    def _invalid_cell(self, cell: Cell) -> None:
        """Raise IndexError if the cell is outside the grid bounds."""
        if cell not in self:
            raise IndexError("Invalid Cell")


class HexGrid(Grid[HexDigit]):
    """Grid of hex digits representing walled cells, displayed as a hex
    string."""
    def __init__(self, size: tuple[int, int],
                 initial_val: HexDigit = 15) -> None:
        """Initialize a hex grid with all walls intact (default value 15)."""
        super().__init__(size, initial_val)

    def __str__(self) -> str:
        """Return the grid as a newline-separated string of uppercase hex
        characters."""
        string: str = ""
        for row in self._data:
            for cell in row:
                string += format(cell, "X")
            string += "\n"
        return string


class BoolGrid(Grid[bool]):
    """Grid of booleans rendered as filled and empty unicode block
    characters."""
    def __str__(self) -> str:
        """Return the grid as a string of block characters, filled for True
        and empty for False."""
        parts: list[str] = []
        for row in self._data:
            for pixel in row:
                parts.append("██" if pixel else "  ")
            parts.append("\n")
        return "".join(parts)


class Maze(HexGrid):
    """Hex grid representing a maze with designated entry and exit cells."""
    def __init__(self, size: tuple[int, int], entry: Cell, exit: Cell):
        """Initialize the maze grid and store the entry and exit cells."""
        super().__init__(size)
        self.entry = entry
        self.exit = exit

    def is_coherent(self) -> bool:
        """Return True if every shared wall between adjacent cells is
        consistent on both sides."""
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
        """Return True if the maze is too small to support the 42 logo
        overlay."""
        return self.height < 7 or self.width < 9

    def is_wall(self, cell: Cell, direction: Direction) -> bool:
        """Return True if there is a wall on the given side of the cell."""
        return is_wall(self[cell], direction)

    def is_closed(self, cell: Cell) -> bool:
        """Return True if all four walls of the cell are intact."""
        return self[cell] == 15

    def _action_wall(self, cell: Cell, dir: Direction,
                     action: Callable[[HexDigit, HexDigit, Direction],
                                      tuple[HexDigit, HexDigit]]) -> None:
        """Apply a wall action function to a cell and its neighbour in the
        given direction."""
        cell2 = cell.neighbour(dir)
        hex1 = self[cell]
        hex2 = self[cell2]
        hex1, hex2 = action(hex1, hex2, dir)
        self[cell] = hex1
        self[cell2] = hex2

    def break_wall(self, cell: Cell, dir: Direction) -> None:
        """Remove the wall between a cell and its neighbour in the given
        direction."""
        self._action_wall(cell, dir, hex_break)

    def build_wall(self, cell: Cell, dir: Direction) -> None:
        """Add a wall between a cell and its neighbour in the given
        direction."""
        self._action_wall(cell, dir, hex_build)

    def flip_wall(self, cell: Cell, dir: Direction) -> None:
        """Toggle the wall between a cell and its neighbour in the given
        direction."""
        self._action_wall(cell, dir, hex_flip)
