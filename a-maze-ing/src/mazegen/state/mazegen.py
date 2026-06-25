"""Module for maze generation, solving, saving, and launching the
interactive curses display."""
from dataclasses import fields
import random
import curses
import sys
from typing import Self
from mazegen.algorithms.maze_generators import (GENERATORS, MazeGenError,
                                                Generator, EntryExitError)
from mazegen.algorithms.solver import bfs, Path
from mazegen.utils.grid import Cell, Maze
from mazegen.parsing.config_parser import MazeConfig, parse_config, ConfigError


class MazeGenerator:
    """Orchestrates maze generation, solving, saving, and display from config
    or direct parameters."""
    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] | Cell, exit: tuple[int, int] | Cell,
                 output_file: str = "output.txt", perfect: bool = True,
                 seed: int | None = None, algorithm: str = "backtracking",
                 forty_two: bool = True) -> None:
        """Validate and store all maze generation parameters, raising an error
        for unsupported algorithms."""
        self.width: int = width
        self.height: int = height
        self.entry: Cell = entry if isinstance(entry, Cell) else Cell(*entry)
        self.exit: Cell = exit if isinstance(exit, Cell) else Cell(*exit)
        self.output_file: str = output_file
        self.perfect: bool = perfect
        self.seed: int | None = seed
        if (alg := GENERATORS.get(algorithm)) is None:
            raise MazeGenError(f"Algorithm not supported. Select from"
                               f" available algorithms:"
                               f"{list(GENERATORS.keys())}")
        self.algorithm: type[Generator] = alg
        self.forty_two: bool = forty_two

    @classmethod
    def from_config(cls, config: MazeConfig) -> Self:
        """Instantiate a MazeGenerator from a MazeConfig dataclass."""
        data = {f.name: getattr(config, f.name) for f in fields(config)}
        return cls(**data)

    def generate(self) -> Maze:
        """Run the selected algorithm to generate and optionally imperfect the
        maze."""
        random.seed(self.seed)
        generator: Generator = self.algorithm(self.height, self.width,
                                              self.entry, self.exit,
                                              self.forty_two)
        generator.generate()
        if not self.perfect:
            generator.imperfect(0.1)
            if generator.has_3x3_empty_area():
                if self.seed is not None:
                    self.seed += 1
                return self.generate()
        return generator.maze

    @staticmethod
    def solve(maze: Maze) -> Path:
        """Solve the maze using BFS and return the solution path."""
        return bfs(maze)

    def save_maze(self, maze: Maze, solution: Path) -> None:
        """Write the maze, entry, exit, and solution directions to the output
        file."""
        with open(self.output_file, "w") as file:
            file.write(str(maze) + '\n')
            file.write(str(maze.entry) + '\n')
            file.write(str(maze.exit) + '\n')
            file.write("".join((str(d.direction) for d in solution)) + '\n')

    @staticmethod
    def _main_run_display(stdscr: curses.window) -> None:
        """Initialize the curses machine from config and run the interactive
        key-input loop."""
        from mazegen.state.machine import Machine
        config: MazeConfig = parse_config(sys.argv[1])
        sys.setrecursionlimit(20000)
        stdscr.refresh()
        machine = Machine(config, stdscr)
        machine.handler("g")
        while (key := machine.maze_win.getkey()) != "q":
            machine.handler(key)

    @staticmethod
    def run_display() -> None:
        """Launch the curses display, catching and printing any generation,
        config, or terminal errors."""
        try:
            curses.wrapper(MazeGenerator._main_run_display)
        except EntryExitError as e:
            print(f"{e} -> Please change entry or exit value")
        except MazeGenError as e:
            print(f"Couldn't generate maze: {e}")
        except curses.error:
            print("Make the terminal bigger, it's too small")
        except ConfigError as e:
            print(f"The config file could't be parsed: {e}")
