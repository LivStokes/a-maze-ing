from contextlib import suppress
from hex_helpers import Direction, is_wall
from grid import Cell, HexGrid, BoolGrid
from geneator_maze import Maze
import curses
from color_palletes import ColorPalette
from dataclasses import dataclass
from typing import Literal
from itertools import cycle
from time import sleep



class MazePrint:
    def __init__(self, maze: Maze, stdscr: curses.window) -> None:
        self.maze = maze
        if not maze.grid.is_coherent():
            raise Exception("Bad grid")
        self.height = maze.grid.height * 2 + 1
        self.width = maze.grid.width * 2 + 1
        self.ascii = BoolGrid((self.height, self.width), False)
        self.stdscr = stdscr

    def create_ascii(self):
        for cell in self.maze.grid:
            for direction in Direction:
                if is_wall(self.maze.grid[cell], direction):
                    self.ascii[self.map_grid(cell).neighbour(direction)] = True
        self._fill_walls()

    def _fill_walls(self):
        for row in range(0, self.height, 2):
            for col in range(0, self.width, 2):
                if self._check_next_walls(cell := Cell(row, col)):
                    self.ascii[cell] = True

    def _check_next_walls(self, cell: Cell):
        for direction in Direction:
            with suppress(IndexError):
                if self.ascii[cell.neighbour(direction)]:
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

    def place_color(self, cell: Cell, color: int, string: str = "██"):
        y, x = cell.row, cell.col * 2
        self.stdscr.addstr(y, x, string, color)
    
    def build_maze(self, color: int):
        self.place_color(Cell(0,0), color, str(self.ascii))
        # for cell in self.ascii:
        #     self.place_color(cell, color, "██" if self.ascii[cell] else "  ")

    def color_list(self, cell_list: list[Cell], color: int):
        cells = (self.map_grid(cell) for cell in cell_list)
        for cell in cells:
            self.place_color(cell, color)

    def display_all(self, pallete: ColorPalette):
        self.build_maze(pallete.walls)
        self.place_color(self.map_grid(self.maze.entry), pallete.entry)
        self.place_color(self.map_grid(self.maze.exit), pallete.exit)
        self.color_list(self.maze.forty_two, pallete.forty_two)
    
    def display_path(self, path: list[tuple[Cell, Direction]], color: int):
        self.place_color(self.map_grid(path[0][0]).neighbour(path[0][1]), color)
        for cell in path[1:]:
            self.place_color(self.map_grid(cell[0]), color)
            self.place_color(self.map_grid(cell[0]).neighbour(cell[1]), color)
    
    def animate_path(self, path: list[tuple[Cell, Direction]], color: int, sleep_time: float = 0.01):
        sleep(sleep_time)
        self.place_color(self.map_grid(path[0][0]).neighbour(path[0][1]), color)
        self.stdscr.refresh()
        for cell in path[1:]:
            sleep(sleep_time)
            self.place_color(self.map_grid(cell[0]), color)
            self.stdscr.refresh()
            sleep(sleep_time)
            self.place_color(self.map_grid(cell[0]).neighbour(cell[1]), color)
            self.stdscr.refresh()








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
