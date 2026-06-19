from contextlib import suppress
from hex_helpers import Direction, is_wall
from grid import Cell, HexGrid, BoolGrid, Maze
import curses
from color_palletes import ColorPalette
from dataclasses import dataclass
from typing import Literal
from itertools import cycle
from time import sleep
from solver import Path



class MazePrint:
    def __init__(self, maze: Maze, stdscr: curses.window) -> None:
        self.maze = maze
        self.height = maze.height * 2 + 1
        self.width = maze.width * 2 + 1
        self.ascii = self.create_ascii(BoolGrid((self.height,
                                                 self.width), False))
        self.closed_cells = [cell for cell in self.maze
                             if self.maze.is_closed(cell)]
        self.stdscr = stdscr
        self.offset = self.calc_offset()

    def create_ascii(self, grid: BoolGrid) -> BoolGrid:
        for cell in self.maze:
            for direction in Direction:
                if is_wall(self.maze[cell], direction):
                    grid[self.map_grid(cell).neighbour(direction)] = True
        self._fill_walls(grid)
        return grid

    def _fill_walls(self, grid: BoolGrid) -> BoolGrid:
        for row in range(0, self.height, 2):
            for col in range(0, self.width, 2):
                if self._check_next_walls(grid, cell := Cell(row, col)):
                    grid[cell] = True
        return grid
    def _check_next_walls(self, grid: BoolGrid, cell: Cell) -> bool:
        for direction in Direction:
            with suppress(IndexError):
                if grid[cell.neighbour(direction)]:
                    return True
        return False

    @staticmethod
    def is_cell(row, col):
        return row % 2 == 1 and col % 2 == 1

    @staticmethod
    def is_in_wall(row, col):
        return row % 2 == 0 and col % 2 == 0

    @staticmethod
    def is_wall(row, col):
        return row % 2 == 1 ^ col % 2 == 1


    def map_grid(self, cell: Cell) -> Cell:
        return Cell(cell.row * 2 + 1, cell.col * 2 + 1)

    def calc_offset(self) -> tuple[int, int]:
        y, x = self.stdscr.getmaxyx()
        return (y - self.height) // 2, (x - self.width*2) // 2

    def place_color(self, cell: Cell, color: int, string: str = "██"):
        y, x = cell.row + self.offset[0], cell.col * 2 + self.offset[1]
        self.stdscr.addstr(y, x, string, color)


    def build_maze(self, color: int):
        for cell in self.ascii:
            self.place_color(cell, color, "██" if self.ascii[cell] else "  ")

    def color_list(self, cell_list: list[Cell], color: int):
        cells = (self.map_grid(cell) for cell in cell_list)
        for cell in cells:
            self.place_color(cell, color)

    def display_all(self, pallete: ColorPalette):
        self.offset = self.calc_offset()
        self.stdscr.clear()
        self.build_maze(pallete.walls)
        self.place_color(self.map_grid(self.maze.entry), pallete.entry)
        self.place_color(self.map_grid(self.maze.exit), pallete.exit)
        self.color_list(self.closed_cells, pallete.forty_two)
        if self.maze.is_small:
            self.place_color(Cell(self.height + 1, 0), curses.A_BOLD,
                             "Maze too small for 42")
    
    def display_path(self, path: Path, color: int):
        self.offset = self.calc_offset()
        self.place_color(self.map_grid(path[0].cell).neighbour(path[0].direction),color)
        for pathbit in path[1:]:
            self.place_color(self.map_grid(pathbit.cell), color)
            self.place_color(self.map_grid(pathbit.cell).neighbour(pathbit.direction), color)
    
    def animate_path(self, path: Path, color: int, sleep_time: float = 0.01):
        self.offset = self.calc_offset()
        sleep(sleep_time)
        self.place_color(self.map_grid(path[0].cell).neighbour(path[0].direction), color)
        self.stdscr.refresh()
        for pathbit in path[1:]:
            sleep(sleep_time)
            self.place_color(self.map_grid(pathbit.cell), color)
            self.stdscr.refresh()
            sleep(sleep_time)
            self.place_color(self.map_grid(pathbit.cell).neighbour(pathbit.direction), color)
            self.stdscr.refresh()
    
    # def show_menu(self, actions: list, color: int):
    #     y, x = self.stdscr.getmaxyx()
    #     f = pyfiglet.Figlet("serifcap")
    #     menu = curses.newwin(30, 30, y-40, x-40)
    #     menu.border()
    #     menu.addstr(f.renderText("HE"), color | curses.A_BOLD)
    #     menu.addstr(f.renderText("LO"), color | curses.A_BOLD)
    #     menu.refresh()



class Menu:
    def __init__(self):
        self.action_strings = {"c": "change color",
                               "s": "solve the maze",
                               "g": "generate new maze",
                               "q": "quit"}
        self.menu_win = curses.newwin(300, 1000, 0,300)
    def write(self, actions: list[str]):
        y = 1
        for action in actions + ["q"]:
            self.menu_win.addstr(figlet_format(f"{action} {self.action_strings[action]}","epic"),
                                 curses.A_BOLD)
            y += 1
    def display(self, actions: list[str]):
        self.menu_win.clear()
        self.write(actions)

menu = Menu()

# text = """9515391539551795151151153
# EBABAE812853C1412BA812812
# 96A8416A84545412AC4282C2A
# C3A83816A9395384453A82D02
# 96842A852AC07AAD13A8283C2
# C1296C43AAB83AA92AA8686BA
# 92E853968428444682AC12902
# AC3814452FA83FFF82C52C42A
# 85684117AFC6857FAC1383D06
# C53AD043AFFFAFFF856AA8143
# 91441294297FAFD501142C6BA
# AA912AC3843FAFFF82856D52A
# 842A8692A92B8517C4451552A
# 816AC384468285293917A9542
# C416928513C443A828456C3BA
# 91416AA92C393A82801553AAA
# A81292AA814682C6A8693C6AA
# A8442C6C2C1168552C16A9542
# 86956951692C1455416928552
# C545545456C54555545444556"""

# test = print_maze(text)
# print("")
# test.create_ascii()
# test.show()
