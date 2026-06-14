from geneator_maze import Maze
from print_maze import MazePrint
from solver import Solver
from grid import Cell
import sys
sys.setrecursionlimit(20000)
gene = Maze((100, 100))
gene.backtracking(gene.entry)
gene.imperfect(0.7)
print(gene.grid)
printer = MazePrint(gene.grid)
printer.create_ascii()
printer.show()
solver = Solver(gene.grid, (Cell(0,0), Cell(99, 99)))
[print(path[1], end='') for path in solver.bfs()]
print()