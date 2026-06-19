from __future__ import annotations
from color_palletes import colors
from print_maze import MazePrint
from grid import Maze
from collections.abc import Callable
from solver import Path
import curses
from config_parser import MazeConfig
from mazegen import MazeGenerator


class Machine:
    def __init__(self, config: MazeConfig, stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        self.config = config
        self.maze_win = stdscr
        self.solution: Path
        self.state: State = Unsolved(self)
        self.displayer: MazePrint
        self.maze: Maze
    
    def handler(self, key: str) -> None:
        if action := self.state.actions.get(key):
            try:
                self.state = action()
            except curses.error:
                self.maze_win.clear()
                self.maze_win.addstr("Screen too small. Please increase size.",
                               curses.A_BOLD | curses.A_BLINK | curses.A_UNDERLINE)
        self.maze_win.refresh()

    def solve(self) -> State:
        self.displayer.animate_path(self.solution, colors.pallete.path, 1 / len(self.solution))
        return Solved(self)

    def change_color(self) -> State:
        self.displayer.display_all(colors.next_pallete())
        if isinstance(self.state, Solved):
            self.displayer.display_path(self.solution,
                                        colors.pallete.path)
        return self.state

    def unsolve(self) -> State:
        self.displayer.display_all(colors.pallete)
        return Unsolved(self)

    def regenerate(self) -> State:
        generator = MazeGenerator.from_config(self.config)
        self.maze = generator.generate()
        self.solution = generator.solve(self.maze)
        generator.save_maze(self.maze, self.solution)
        self.displayer = MazePrint(self.maze, self.maze_win)
        self.displayer.display_all(colors.pallete)
        return Unsolved(self)
    
class State:
    def __init__(self, machine: Machine):
        self.machine: Machine = machine
        self.actions: dict[str, Callable[[], State]]

class Unsolved(State):
    def __init__(self, machine: Machine):
        self.actions = {"c": machine.change_color,
                        "g": machine.regenerate,
                        "s": machine.solve}
        super().__init__(machine)

class Solved(State):
    def __init__(self, machine: Machine):
        self.actions = {"c": machine.change_color,
                        "g": machine.regenerate,
                        "s": machine.unsolve}
        super().__init__(machine)
