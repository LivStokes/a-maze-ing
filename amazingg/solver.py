from grid import Grid, Cell
from hex_helpers import Direction, is_wall
from collections import deque

class Solver():
    def __init__(self, grid: Grid, entry_exit: tuple[Cell, Cell]):
        self.entry, self.exit = entry_exit
        self.grid = grid
    
    def bfs(self) -> list[tuple[Cell, Direction]]:
        queue: deque[Cell] = deque()
        queue.append(self.entry)
        parent: dict[Cell, tuple[Cell, Direction] | None] = {self.entry: None}
        while queue:
            current: Cell = queue.popleft()
            if current == self.exit:
                break
            for direction in Direction:
                if not (is_wall(self.grid[current], direction) or
                     (neighbour := current.neighbour(direction)) in parent):
                    parent[neighbour] = current, direction
                    queue.append(neighbour)
        if current != self.exit:
            raise Exception("Path not found")
        path: list[tuple[Cell, Direction]] = []
        while parent[current]:
            path.append(parent[current])
            current = parent[current][0]
        path.reverse()
        return path



