from contextlib import suppress
from hex_helpers import Direction, is_wall
from grid import Cell, Grid


class MazePrint:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        if not grid.is_coherent():
            raise Exception("Bad grid")
        self.height = self.grid.height * 2 + 1
        self.width = self.grid.width * 2 + 1
        self.ascii = [[False] * self.width for _ in range(self.height)]

    def create_ascii(self):
        for cell in self.grid:
            for direction in Direction:
                if is_wall(self.grid[cell], direction):
                    row_ascii, col_ascii = self.map_grid(cell, direction)
                    self.ascii[row_ascii][col_ascii] = True
        self.fill_walls()

    def fill_walls(self):
        for row in range(0, self.height, 2):
            for col in range(0, self.width, 2):
                if self.check_next_walls(row, col):
                    self.ascii[row][col] = True

    def check_next_walls(self, row: int, col: int):
        for wall in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            with suppress(IndexError):
                if self.ascii[row + wall[0]][col + wall[1]]:
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

    def map_grid(self, cell: Cell, direction: Direction) -> tuple[int, int]:
        match direction:
            case Direction.N:
                return cell.row * 2, cell.col * 2 + 1
            case Direction.E:
                return cell.row * 2 + 1, cell.col * 2 + 2
            case Direction.S:
                return cell.row * 2 + 2, cell.col * 2 + 1
            case Direction.W:
                return cell.row * 2 + 1, cell.col * 2

    def show(self):
        for row in self.ascii:
            for pixel in row:
                if pixel:
                    print("██", end="")
                else:
                    print("  ", end="")
            print("")


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
