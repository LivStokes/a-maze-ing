from grid import Cell, Maze
from hex_helpers import Direction
from random import sample, random, choice
from contextlib import suppress
from dataclasses import asdict, astuple, fields
import random
from abc import ABC, abstractmethod
from solver import Path, bfs

class MazeGenError(Exception):
    pass

class EntryExitError(MazeGenError):
    pass


class Generator(ABC):
    def __init__(self, height: int, width: int, entry: Cell, exit: Cell, ft: bool):
        super().__init__()
        self.maze = Maze((height, width), entry, exit)
        self.forty_two = self._forty_two(ft)
        self._entry_exit_raises()

    def _forty_two(self, ft) -> list[Cell]:
        if self.maze.is_small or not ft:
            return []
        middle_cell = Cell(self.maze.height // 2, self.maze.width // 2)
        forty_two_vectors = [(0, -1), (0, -2), (0, -3), (-1, -3), (-2, -3),
                             (1, -1), (2, -1), (0, 1), (0, 2), (0, 3), (1, 1),
                             (2, 1), (2, 2), (2, 3), (-1, 3), (-2, 3), (-2, 2),
                             (-2, 1)]
        return [middle_cell + vector for vector in forty_two_vectors]

    def _entry_exit_raises(self) -> None:
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
        for cell in self.maze:
            if cell not in self.forty_two and random() < likelyhood:
                direction = choice(list(Direction))
                if (cell.neighbour(direction) not in self.forty_two and
                    cell.neighbour(direction) in self.maze):
                    self.maze.break_wall(cell, direction)

    @abstractmethod
    def generate(self):
        pass

class BacktrackingGenerator(Generator):
    def _hasnt_been_visited(self, cell: Cell) -> bool:
        return self.maze[cell] == 15

    def generate(self, cell: Cell = Cell(0, 0)):
        for dir in sample(list(Direction), k=len(Direction)):
            with suppress(IndexError):
                if (self._hasnt_been_visited(cell.neighbour(dir)) and
                    cell.neighbour(dir) not in self.forty_two):
                    self.maze.break_wall(cell, dir)
                    self.generate(cell.neighbour(dir))

class PrimsGenerator(Generator):
    """
    Maze generator using randomised Prim's algorithm.
    Prim's algorithm is a minimum spanning tree algorithm apted for maze generation. 
    It grows the maze outward from a single seed cell by maintaining a frontier.
    The frontier is a list of (unvisited_cell, visited_neighbour, direction) tuples representing every wall on the boundary of the already-visited region.
    At each step, a random entry is chosen from the frontier.
    If the candidate has already been visited by a different frontier, it is discarded.
    This continues until the frontier is empty and every cell is connected.
    Cells belonging to the '42' pattern inherited from 'Generator' are never added to the frontier.

    Result
    ------
    A perfect Maze (spanning tree of the grid).
    """
    def _unvisited(self, cell: Cell) -> bool:
        """
        Parameters
        ----------
        cell : Cell
            The cell to check.

        Returns
        -------
        bool
            True if unvisited, False otherwise.

        """
        return self.maze[cell] == 15

    def _add_frontier(self, frontier: list[tuple[Cell, Cell, Direction]], cell: Cell) -> None:
        """

        """
        for direction in Direction:
            neighbour = cell.neighbour(direction)
            if (neighbour in self.maze
                and neighbour not in self.forty_two
                and self._unvisited(neighbour)):
                frontier.append((neighbour, cell, direction))

    def generate(self, start: Cell | None = None) -> None:
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


generators: dict[str, type[Generator]]
generators = {"backtracking":BacktrackingGenerator, "prims": PrimsGenerator}
