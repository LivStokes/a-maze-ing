from random import sample, random, choice
from contextlib import suppress
from abc import ABC, abstractmethod
from mazegen.utils.grid import Cell, Maze
from mazegen.utils.hex_helpers import Direction


class MazeGenError(Exception):
    """Base exception class for maze generation errors."""
    pass


class EntryExitError(MazeGenError):
    """Exception raised for invalid maze entry or exit configurations."""
    pass


class Generator(ABC):
    """Abstract base ckass for maze generation algorithms."""
    def __init__(self, height: int, width: int, entry: Cell, exit: Cell,
                 ft: bool) -> None:
        """Initialize the maze generator with grid dimensions, entry/exit
        points, and logo overlay preference."""
        super().__init__()
        self.maze = Maze((height, width), entry, exit)
        self.forty_two = self._forty_two(ft)
        self._entry_exit_raises()

    def _forty_two(self, ft: bool) -> list[Cell]:
        """Generate the list of cells that form the '42' logo mask overlay."""
        if self.maze.is_small or not ft:
            return []
        middle_cell = Cell(self.maze.height // 2, self.maze.width // 2)
        forty_two_vectors = [(0, -1), (0, -2), (0, -3), (-1, -3), (-2, -3),
                             (1, -1), (2, -1), (0, 1), (0, 2), (0, 3), (1, 1),
                             (2, 1), (2, 2), (2, 3), (-1, 3), (-2, 3), (-2, 2),
                             (-2, 1)]
        return [middle_cell + vector for vector in forty_two_vectors]

    def _entry_exit_raises(self) -> None:
        """Validate that the entry and exit points are positioned legally
        within the maze bounds and masks."""
        if self.maze.entry in self.forty_two:
            raise EntryExitError("Entry inside forty two logo")
        if self.maze.exit in self.forty_two:
            raise EntryExitError("Exit inside forty two logo")
        if self.maze.entry not in self.maze:
            raise EntryExitError("Entry is outside the maze.")
        if self.maze.exit not in self.maze:
            raise EntryExitError("Exit is outide the maze.")
        if self.maze.exit == self.maze.entry:
            raise EntryExitError("Entry is the same as exit")

    def imperfect(self, likelyhood: float = 0.1) -> None:
        """Introduce loops into the maze by randomly breaking walls down based
        on a likelyhood threshold."""
        for cell in self.maze:
            if cell not in self.forty_two and random() < likelyhood:
                direction = choice(list(Direction))
                if (cell.neighbour(direction) not in self.forty_two and
                   cell.neighbour(direction) in self.maze):
                    self.maze.break_wall(cell, direction)

    def has_3x3_empty_area(self) -> bool:
        """Checks if the maze contains 3x3 empty areas"""
        for row in range(1, self.maze.height - 1):
            for col in range(1, self.maze.width - 1):
                cell = Cell(row, col)
                if self._3x3_is_empty(cell):
                    return True
        return False

    def _3x3_is_empty(self, cell: Cell) -> bool:
        """Checks if a 3x3 area is empty"""
        for direction in Direction:
            for dir in Direction:
                if dir == direction:
                    continue
                if self.maze.is_wall(cell.neighbour(direction), dir):
                    return False
        return True

    @abstractmethod
    def generate(self) -> None:
        """Abstract method to execute the specific maze generation algorthm."""
        pass


class BacktrackingGenerator(Generator):
    """Maze generator that utilizes a recursive backtracking (DFS) approach."""
    def _hasnt_been_visited(self, cell: Cell) -> bool:
        """Check if a given cell has all of its initial walls intact,
        inficating it is unvisited."""
        return self.maze[cell] == 15

    def generate(self, cell: Cell = Cell(0, 0)) -> None:
        """Recursively generate the maze using depth-first search starting
        from the specified cell."""
        for dir in sample(list(Direction), k=len(Direction)):
            with suppress(IndexError):
                if (self._hasnt_been_visited(cell.neighbour(dir)) and
                   cell.neighbour(dir) not in self.forty_two):
                    self.maze.break_wall(cell, dir)
                    self.generate(cell.neighbour(dir))


class PrimsGenerator(Generator):
    """Maze generator that utilizes a randomized variation of Prim's
    algorithm."""
    def _unvisited(self, cell: Cell) -> bool:
        """Check if a given cell remains unvisited by verifying its walls
        are fully intact."""
        return self.maze[cell] == 15

    def _add_frontier(self, frontier: list[tuple[Cell, Cell, Direction]],
                      cell: Cell) -> None:
        """finds valid, unvisited neighbours of a cell and adds them to the
        frontier list."""
        for direction in Direction:
            neighbour = cell.neighbour(direction)
            if (neighbour in self.maze
               and neighbour not in self.forty_two
               and self._unvisited(neighbour)):
                frontier.append((neighbour, cell, direction))

    def generate(self, start: Cell | None = None) -> None:
        """Generate the maze by expanding randomly across a growing frontier
        of unvisited cells"""
        if start is None:
            start = self.maze.entry
        frontier: list[tuple[Cell, Cell, Direction]] = []
        self._add_frontier(frontier, start)
        while frontier:
            idx = choice(range(len(frontier)))
            candidate, from_cell, direction = frontier[idx]
            frontier[idx] = frontier[-1]
            frontier.pop()
            if not self._unvisited(candidate):
                continue
            self.maze.break_wall(from_cell, direction)
            self._add_frontier(frontier, candidate)


GENERATORS: dict[str, type[Generator]]
GENERATORS = {"backtracking": BacktrackingGenerator, "prims": PrimsGenerator}
