from time import sleep
import curses
def main(stdscr: curses.window):
    from machine import Machine
    from geneator_maze import Maze
    from print_maze import MazePrint
    from grid import Cell
    import sys
    sys.setrecursionlimit(20000)
    machine = Machine((100,100), (Cell(1, 4), Cell(29, 39)), stdscr)
    machine.handler("g")
    stdscr.refresh()
    while (key := stdscr.getkey()) != "q":
        machine.handler(key)
        # stdscr.refresh


if __name__ == '__main__':
    curses.wrapper(main)