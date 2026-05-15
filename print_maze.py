from contextlib import suppress

N = 0
E = 1
S = 2
W = 3

class print_maze:
    def __init__(self, maze: str, dimensions: tuple[int, int]) -> None:
        self.maze = maze
        self.dim = dimensions
    
    def create_ascii(self):
        rows = self.dim[0]*2 + 1
        columns = self.dim[1]*2 + 1
        maze_list = self.maze.split(sep="\n")
        print(maze_list)
        self.ascii = [[False] * columns for _ in range(rows)]
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                for bit in range(4):
                    if (int(maze_list[row][col], 16) >> bit) & 1:
                        row_ascii, col_ascii = self.map_grid(row, col, bit)
                        self.ascii[row_ascii][col_ascii] = True
        self.fill_walls(rows, columns)


    def fill_walls(self, rows: int, cols: int):
        for row in range(0, rows, 2):
            for col in range(0, cols, 2):
                if self.check_next_walls(row, col):
                        self.ascii[row][col] = True

    def check_next_walls(self, row: int, col: int):
        count = 0
        for wall in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            with suppress(IndexError):
                if self.ascii[row + wall[0]][col + wall[1]]:
                    count += 1
            if count >= 2:
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


    def map_grid(self, row: int, col: int, bit: int) -> tuple[int, int]:
        if bit == N:
            return row*2, col*2 + 1
        if bit == E:
            return row*2 + 1, col * 2 + 2
        if bit == S:
            return row*2 + 2, col*2 + 1
        if bit == W:
            return row*2 + 1, col*2
    
    def show(self):
        for row in self.ascii:
            for cell in row:
                if cell:
                    print("██", end="")
                else:
                    print("  ", end="")
            print("")

text ="""9515391539551795151151153
EBABAE812853C1412BA812812
96A8416A84545412AC4282C2A
C3A83816A9395384453A82D02
96842A852AC07AAD13A8283C2
C1296C43AAB83AA92AA8686BA
92E853968428444682AC12902
AC3814452FA83FFF82C52C42A
85684117AFC6857FAC1383D06
C53AD043AFFFAFFF856AA8143
91441294297FAFD501142C6BA
AA912AC3843FAFFF82856D52A
842A8692A92B8517C4451552A
816AC384468285293917A9542
C416928513C443A828456C3BA
91416AA92C393A82801553AAA
A81292AA814682C6A8693C6AA
A8442C6C2C1168552C16A9542
86956951692C1455416928552
C545545456C54555545444556"""

test = print_maze(text, (20 ,25))
print("")
test.create_ascii()
test.show()