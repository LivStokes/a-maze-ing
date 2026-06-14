from color_palletes import colors
from geneator_maze import Maze
from print_maze import MazePrint
from grid import Cell
from hex_helpers import Direction
from collections.abc import Callable
from solver import bfs, Path
import curses


class Machine:
    def __init__(self, size: tuple[int, int], entry_exit: tuple[Cell, Cell], stdscr: curses.window):
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        self.size = size
        self.entry_exit = entry_exit
        self.stdscr = stdscr
        self.state: State = Unsolved(self)
        self.displayer: MazePrint
        self.maze_gene: Maze

    def handler(self, key: str):
        if action := self.state.actions.get(key):
            action()

    def solve(self):
        solution = bfs(self.maze_gene.grid, self.entry_exit)
        self.displayer.animate_path(solution, colors.pallete.path, 1 / len(solution))
        self.state = Solved(self, solution)
    
    def change_color(self):
        # self.stdscr.clear()
        self.displayer.display_all(colors.next_pallete())
        if isinstance(self.state, Solved):
            self.displayer.display_path(self.state.solution,
                                        colors.pallete.path)

    def regenerate(self):
        # self.stdscr.clear()
        self.maze_gene = Maze(self.size, self.entry_exit)
        self.maze_gene.backtracking()
        self.maze_gene.imperfect()
        self.displayer = MazePrint(self.maze_gene, self.stdscr)
        self.displayer.create_ascii()
        self.displayer.display_all(colors.pallete)
        self.state = Unsolved(self)



class State:
    def __init__(self, machine: Machine):
        self.machine: Machine = machine
        self.actions: dict[str, Callable[[], None]] = {}

class Unsolved(State):
    def __init__(self, machine: Machine):
        super().__init__(machine)
        self.actions = {"c": self.machine.change_color,
                        "g": self.machine.regenerate,
                        "s": self.machine.solve}

class Solved(State):
    def __init__(self, machine: Machine, solution: Path):
        super().__init__(machine)
        self.solution = solution
        self.actions = {"c": self.machine.change_color,
                        "g": self.machine.regenerate}
