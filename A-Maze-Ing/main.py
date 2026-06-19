import curses
from maze_generators import EntryExitError
from config_parser import parse_config, ConfigError
from maze_generators import EntryExitError
import sys
from pathlib import Path


def main(stdscr: curses.window):
    from machine import Machine
    #config = MazeConfig(50, 50, Cell(0,0), Cell(49,49), "output.txt", True, None, "prims", True)
    sys.setrecursionlimit(20000)
    stdscr.refresh()
    machine = Machine(config, stdscr)
    machine.handler("g")
    while (key := machine.maze_win.getkey()) != "q":
            machine.handler(key)


if __name__ == '__main__':
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    try:
        config = parse_config(Path(config_path))
    except ConfigError as e:
        print(f"Config error: {e}")
        sys.exit(1)
    try:
        curses.wrapper(main)
    except EntryExitError as e:
         print(f"{e} -> Please change entry or exit value")
    except curses.error:
         print(f"Make the terminal bigger, it's too small")
