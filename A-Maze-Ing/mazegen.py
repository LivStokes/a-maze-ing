from grid import Cell, Maze
from maze_generators import generators
from config_parser import MazeConfig
from solver import bfs, Path
from dataclasses import fields
import random


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] | Cell, exit: tuple[int, int] | Cell,
                 output_file: str = "output.txt", perfect: bool = True,
                 seed: int | None = None, algorithm: str = "backtracking",
                 forty_two: bool = True):
        self.width = width
        self.height = height
        self.entry: Cell = entry if isinstance(entry, Cell) else Cell(*entry)
        self.exit: Cell = exit if isinstance(exit, Cell) else Cell(*exit)
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.algorithm = generators.get(algorithm)
        self.forty_two = forty_two
        # self._entry_exit_raises()

    @classmethod
    def from_config(cls, config: MazeConfig):
        data = {f.name: getattr(config, f.name) for f in fields(config)}
        return cls(**data)
    
    def generate(self) -> Maze:
        random.seed(self.seed)
        generator = self.algorithm(self.height, self.width,
                                   self.entry, self.exit, self.forty_two)
        generator.generate()
        if not self.perfect:
            generator.imperfect()
        return generator.maze

    @staticmethod
    def solve(maze: Maze) -> Path:
        return bfs(maze)
    
    def save_maze(self, maze: Maze, solution: Path):
        with open(self.output_file, "w") as file:
            file.write(str(maze)+'\n')
            file.write(str(maze.entry)+'\n')
            file.write(str(maze.exit)+'\n')
            file.write(str(solution)+'\n')
