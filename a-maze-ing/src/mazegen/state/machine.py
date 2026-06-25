from __future__ import annotations
from collections.abc import Callable
import curses
from .mazegen import MazeGenerator
from mazegen.displayer.color_palletes import COLORS
from mazegen.displayer.print_maze import MazePrint
from mazegen.utils.grid import Maze
from mazegen.algorithms.solver import Path
from mazegen.parsing.config_parser import MazeConfig


class Machine:
    """Manages maze state, user input handling, and display rendering via
    curses."""
    def __init__(self, config: MazeConfig, stdscr: curses.window) -> None:
        """Initialize curses settings, maze configuration, and default state."""
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
        """Dispatch a keypress to the current state's action map and refresh
        the display."""
        if action := self.state.actions.get(key):
            try:
                self.state = action()
            except curses.error:
                self.maze_win.clear()
                self.maze_win.addstr("Screen too small. Please increase size.",
                                     (curses.A_BOLD | curses.A_BLINK
                                      | curses.A_UNDERLINE))
        self.maze_win.refresh()

    def solve(self) -> State:
        """Animate the solution path and transition to the Solved state."""
        self.displayer.animate_path(self.solution, COLORS.pallete.path,
                                    1 / len(self.solution))
        return Solved(self)

    def change_color(self) -> State:
        """Cycle to the next color palette and redisplay the maze and any
        active solution."""
        self.displayer.display_all(COLORS.next_pallete())
        if isinstance(self.state, Solved):
            self.displayer.display_path(self.solution,
                                        COLORS.pallete.path)
        return self.state

    def unsolve(self) -> State:
        """Redisplay the maze without the solution path and transition to the
        Unsolved state."""
        self.displayer.display_all(COLORS.pallete)
        return Unsolved(self)

    def regenerate(self) -> State:
        """Generate a new maze and solution, update the display, and return to
        Unsolved state."""
        generator = MazeGenerator.from_config(self.config)
        self.maze = generator.generate()
        self.solution = generator.solve(self.maze)
        generator.save_maze(self.maze, self.solution)
        self.displayer = MazePrint(self.maze, self.maze_win)
        self.displayer.display_all(COLORS.pallete)
        return Unsolved(self)


class State:
    """Base class representing a maze interaction state with an associated
    action map."""
    def __init__(self, machine: Machine):
        """Store the machine reference and define the keybind-to-action
        mapping."""
        self.machine: Machine = machine
        self.actions: dict[str, Callable[[], State]]


class Unsolved(State):
    """State representing an unsolved maze, with actions to color,
    regenerate, or solve."""
    def __init__(self, machine: Machine):
        """Bind keys for color change, regeneration, and solving, then
        initialize base state."""
        self.actions = {"c": machine.change_color,
                        "g": machine.regenerate,
                        "s": machine.solve}
        super().__init__(machine)


class Solved(State):
    """State representing a solved maze, with actions to color, regenerate,
    or unsolve."""
    def __init__(self, machine: Machine):
        """Bind keys for color change, regeneration, and unsolving, then
        initialize base state."""
        self.actions = {"c": machine.change_color,
                        "g": machine.regenerate,
                        "s": machine.unsolve}
        super().__init__(machine)
