from grid import Maze, Cell
from hex_helpers import Direction, is_wall
from collections import deque
from typing import NewType
from dataclasses import dataclass,field

type Path = list[Path_bit]

@dataclass
class Path_bit:
    cell: Cell
    direction: Direction


class PathError(Exception):
    pass

def bfs(maze: Maze) -> Path:
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
    while parent[current]:
        path.append(parent[current])
        current = parent[current].cell
    path.reverse()
    return path



