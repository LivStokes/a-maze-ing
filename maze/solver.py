from grid import HexGrid, Cell
from hex_helpers import Direction, is_wall
from collections import deque
from typing import NewType

Path = NewType('Path', list[tuple[Cell, Direction]])

def bfs(grid: HexGrid,
        entry_exit: tuple[Cell, Cell]) -> Path:
    entry, exit = entry_exit
    queue: deque[Cell] = deque()
    queue.append(entry)
    parent: dict[Cell, tuple[Cell, Direction] | None] = {entry: None}
    current: Cell = entry
    while queue:
        current = queue.popleft()
        if current == exit:
            break
        for direction in Direction:
            if not (is_wall(grid[current], direction) or
                    (neighbour := current.neighbour(direction)) in parent):
                parent[neighbour] = current, direction
                queue.append(neighbour)
    if current != exit:
        raise Exception("Path not found")
    path: Path = []
    while parent[current]:
        path.append(parent[current])
        current = parent[current][0]
    path.reverse()
    return path



