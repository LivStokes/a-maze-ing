import curses
from time import sleep
from contextlib import suppress
from .color_palletes import ColorPalette
from mazegen.utils.hex_helpers import Direction, is_wall
from mazegen.utils.grid import Cell, BoolGrid, Maze
from mazegen.algorithms.solver import Path


class MazePrint:
    """Handles upscale rendering and drawing of the maze onto a curses window
    screen."""
    def __init__(self, maze: Maze, stdscr: curses.window) -> None:
        """Initialize the printer by upscaling the maze dimensions and
        pre-generating the wall ASCII grid."""
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
        """Translate the maze cell wall configurations into an upscaled
        boolean grid layout."""
        for cell in self.maze:
            for direction in Direction:
                if is_wall(self.maze[cell], direction):
                    grid[self.map_grid(cell).neighbour(direction)] = True
        self._fill_walls(grid)
        return grid

    def _fill_walls(self, grid: BoolGrid) -> BoolGrid:
        """Fill in orphan corner wall intersections to ensure the upscaled
        wall rendering looks continuous."""
        for row in range(0, self.height, 2):
            for col in range(0, self.width, 2):
                if self._check_next_walls(grid, cell := Cell(row, col)):
                    grid[cell] = True
        return grid

    def _check_next_walls(self, grid: BoolGrid, cell: Cell) -> bool:
        """Return True if any immediate neighbors of the specified cell
        are flagged as walls."""
        for direction in Direction:
            with suppress(IndexError):
                if grid[cell.neighbour(direction)]:
                    return True
        return False

    @staticmethod
    def is_cell(row: int, col: int) -> bool:
        """Determine if an upscaled coordinate pair maps directly onto a maze
        path cell."""
        return row % 2 == 1 and col % 2 == 1

    @staticmethod
    def is_in_wall(row: int, col: int) -> bool:
        """Determine if an upscaled coordinate pair maps onto a corner wall
        intersection point."""
        return row % 2 == 0 and col % 2 == 0

    @staticmethod
    def is_wall(row: int, col: int) -> bool:
        """Determine if an upscaled coordinate pair maps onto a wall boundary
        line between cells."""
        return row % 2 == 1 ^ col % 2 == 1

    def map_grid(self, cell: Cell) -> Cell:
        """Map a logical maze cell coordinate to its upscaled cell index
        position on the display grid."""
        return Cell(cell.row * 2 + 1, cell.col * 2 + 1)

    def calc_offset(self) -> tuple[int, int]:
        """Calculate the top-left centering offsets required to keep the
        maze centered in the window."""
        y, x = self.stdscr.getmaxyx()
        return (y - self.height) // 2, (x - self.width * 2) // 2

    def place_color(self, cell: Cell, color: int, string: str = "██") -> None:
        """Draw a text string at a cell's offset-adjusted terminal screen
        position using specified colors."""
        y, x = cell.row + self.offset[0], cell.col * 2 + self.offset[1]
        self.stdscr.addstr(y, x, string, color)

    def build_maze(self, color: int) -> None:
        """Iterate through the upscaled boolean grid to draw full wall blocks
        and open pathways."""
        for cell in self.ascii:
            self.place_color(cell, color, "██" if self.ascii[cell] else "  ")

    def color_list(self, cell_list: list[Cell], color: int) -> None:
        """Apply a specified color pair overlay to an entire batch of logical
        maze cells."""
        cells = (self.map_grid(cell) for cell in cell_list)
        for cell in cells:
            self.place_color(cell, color)

    def display_all(self, pallete: ColorPalette) -> None:
        """Clear the window and perform a complete redraw of the maze
        structure, points, and logo masks."""
        self.offset = self.calc_offset()
        self.stdscr.clear()
        self.build_maze(pallete.walls)
        self.place_color(self.map_grid(self.maze.entry), pallete.entry)
        self.place_color(self.map_grid(self.maze.exit), pallete.exit)
        self.color_list(self.closed_cells, pallete.forty_two)
        if self.maze.is_small:
            self.place_color(Cell(self.height + 1, 0), curses.A_BOLD,
                             "Maze too small for 42")

    def display_path(self, path: Path, color: int) -> None:
        """Instantly draw a solved path line connecting path components on
        the maze grid."""
        self.offset = self.calc_offset()
        self.place_color(self.map_grid(path[0].cell)
                         .neighbour(path[0].direction), color)
        for pathbit in path[1:]:
            self.place_color(self.map_grid(pathbit.cell), color)
            self.place_color(self.map_grid(pathbit.cell)
                             .neighbour(pathbit.direction), color)

    def animate_path(self, path: Path, color: int,
                     sleep_time: float = 0.01) -> None:
        """Draw a solved path step-by-step with configured frame delays to
        create a tracing animation."""
        self.offset = self.calc_offset()
        sleep(sleep_time)
        self.place_color(self.map_grid(path[0].cell)
                         .neighbour(path[0].direction), color)
        self.stdscr.refresh()
        for pathbit in path[1:]:
            sleep(sleep_time)
            self.place_color(self.map_grid(pathbit.cell), color)
            self.stdscr.refresh()
            sleep(sleep_time)
            self.place_color(self.map_grid(pathbit.cell)
                             .neighbour(pathbit.direction), color)
            self.stdscr.refresh()
