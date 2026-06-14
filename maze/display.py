import curses
from geneator_maze import Maze
from print_maze import MazePrint, ColorManager
from solver import Solver
from grid import Cell
from random import choice, randint
import sys


sys.setrecursionlimit(20000)
def main(stdscr: curses.window):

    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.use_default_colors()
    stdscr.refresh()
    color = ColorManager()
    color.new_pallete(color.get(curses.COLOR_RED, curses.COLOR_CYAN),
                      color.get(curses.COLOR_GREEN),
                      color.get(curses.COLOR_WHITE),
                      color.get(curses.COLOR_BLUE),
                      color.get(curses.COLOR_YELLOW))
    color.new_pallete(color.get(curses.COLOR_BLACK, curses.COLOR_WHITE),
                      color.get(curses.COLOR_GREEN),
                      color.get(curses.COLOR_RED),
                      color.get(curses.COLOR_BLUE),
                      color.get(curses.COLOR_YELLOW))
    while True:
        stdscr.clear()
        size = 100, 100
        entry = Cell(*(randint(0, x - 1) for x in size))
        exit = Cell(*(randint(0, x - 1) for x in size))
        gene = Maze(size, (entry, exit))
        gene.backtracking(gene.entry)
        gene.imperfect()
        printer = MazePrint(gene, stdscr)
        pallete = choice(color.palletes)
        solver = Solver(gene.grid, (gene.entry, gene.exit))
        printer.create_ascii()
        printer.display_all(pallete)
        # mapped_entry_cell = printer.map_grid(gene.entry)
        # mapped_exit_cell = printer.map_grid(gene.entry)
        # stdscr.addnstr(printer.map_grid(gene.entry))
        stdscr.refresh()
        printer.animate_path(solver.bfs(), pallete.path)
        stdscr.getch()


match key:
    case 'c':
        pallete = next(color.pallete_cycler)


if __name__ == '__main__':
    curses.wrapper(main)