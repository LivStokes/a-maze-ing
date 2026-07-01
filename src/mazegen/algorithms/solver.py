from collections import deque
from dataclasses import dataclass
from mazegen.utils.grid import Maze, Cell
from mazegen.utils.hex_helpers import Direction

type Path = list[Path_bit]


@dataclass
class Path_bit:
    """Represents a single step in a path, pairing a cell with the direction
    taken to leave it"""
    cell: Cell
    direction: Direction


class PathError(Exception):
    """Exeption raised when a valid path cannot be found through the maze"""
    pass


def bfs(maze: Maze) -> Path:
    """Find the shortest path from the maze entry to exit using a
    Breadth-First Search algorithm"""
    entry, exit = maze.entry, maze.exit
    queue: deque[Cell] = deque()
    queue.append(entry)
    parent: dict[Cell, Path_bit | None] = {entry: None}
    current: Cell = entry
    while queue:
        current = queue.popleft()
        if current == exit:
            break
        for direction in Direction:
            if not (maze.is_wall(current, direction) or
                    (neighbour := current.neighbour(direction)) in parent):
                parent[neighbour] = Path_bit(current, direction)
                queue.append(neighbour)
    if current != exit:
        raise PathError("Path not found")
    path: Path = []
    while (step := parent[current]) is not None:
        path.append(step)
        current = step.cell
    path.reverse()
    return path
