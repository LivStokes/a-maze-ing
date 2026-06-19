*This project has been created as part of the 42 curriculum by mmelo, and olistoke*

## Description
A-Maze-ing is a Python maze generator and visualiser.
Given a configuration file, it generates a maze of arbitrary size, optionally enforcing the *perfect maze* property (exactly one path between any two cells).
The maze is rendered interactively in the terminal using curses, and the output is written to a file using a hexadecimal wall encoding.
A hidden **"42"** pattern is embedded in every maze large enough to contain it.

## Instructions
### Requirements
- Python 3.10 or later
- A terminal that supports curses (standard on Linux/macOS)

### How to Install
# Create a virtual environment and install dev dependencies
make install

### How to run
# Run with the default config file
make run

# Or specify your own config file
python3 a_maze_ing.py my_config.txt

### Keyboard controls
Key and Action
`g` = Re-generate a new maze
`s` = Show / hide the shortest path
`c` = Cycle through wall colour palettes
`q` = Quit

### Debug mode
make debug

### Linting
make lint         # flake8 + mypy (standard flags)
make lint-strict  # flake8 + mypy --strict

### Cleaning
make clean

## Configuration file
The config file uses one `KEY=VALUE` pair per line. 
Lines beginning with `#` are comments and are ignored. 
All keys are case-insensitive.

### Required keys
Key > Type > Description > Example
`WIDTH` > positive int > Number of columns in the maze > `WIDTH=20`
`HEIGHT` > positive int > Number of rows in the maze > `HEIGHT=15`
`ENTRY` > `x,y` > Entry cell coordinates (col, row) > `ENTRY=0,0`
`EXIT` > `x,y` > Exit cell coordinates (col, row) > `EXIT=19,14`
`OUTPUT_FILE` > string > Path of the hex-encoded output file > `OUTPUT_FILE=maze.txt`
`PERFECT` > bool > Enforce a single path between entry and exit > `PERFECT=True`

### Optional keys
Key > Type > Default > Description
`SEED` > int > *(random)* > RNG seed for reproducible mazes
`ALGORITHM` > string > `backtracking` > Generation algorithm (`backtracking`)
`IMPERFECT_RATE` > float 0–1 > `0.1` > Probability of removing extra walls when `PERFECT=False`

### Example config
# A-Maze-ing configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=backtracking
IMPERFECT_RATE=0.1

## Maze generation algorithm
This project uses **recursive backtracking** (also known as depth-first search maze generation).

### How it works
Starting from the entry cell, the algorithm visits unvisited neighbours in a random order, breaking the shared wall to connect them, and recurses into each. When no unvisited neighbours remain, it backtracks. The result is a *spanning tree* of the grid — a perfect maze.
If `PERFECT=False`, a post-processing pass randomly removes additional walls with probability `IMPERFECT_RATE`, creating loops and multiple paths.

### Why this algorithm?
- **Simplicity**: the recursive implementation maps cleanly onto the hexadecimal cell representation already used in this project.
- **Quality**: it produces mazes with long, winding corridors and few dead ends — visually interesting and challenging to solve.
- **Speed**: it runs in O(n) time and memory relative to the number of cells.
- **Reproducibility**: seeding Python's `random` module before generation makes any maze fully reproducible.

## Output file format
Each cell is written as one uppercase hexadecimal digit encoding its four walls as bits:
Bit | Direction
0 (LSB) | North
1 | East
2 | South
3 | West
A bit of `1` means the wall is **closed**; `0` means **open**.
Cells are written row by row, one row per line. After an empty line, three additional lines follow:

1. Entry coordinates (`col,row`)
2. Exit coordinates (`col,row`)
3. Shortest path from entry to exit as a sequence of `N`, `E`, `S`, `W` characters
All lines end with `\n`.

## Code reusability
The maze generation logic lives in `geneator_maze.py` as the `Maze` class. It is designed to be used independently of the display layer.

### Quick-start example
from geneator_maze import Maze
from grid import Cell
from random import seed
seed(42)

# Create a 20×15 maze with entry at top-left and exit at bottom-right
maze = Maze(
    size=(15, 20),
    entry_exit=(Cell(0, 0), Cell(14, 19)),
)

# Generate a perfect maze using recursive backtracking
maze.backtracking()

# Optionally remove some walls to make it imperfect (10 % probability)
maze.imperfect(likelyhood=0.1)

# Access the hex grid
print(maze.grid)          # HexGrid — one hex digit per cell

# Access metadata
print(maze.entry)         # Cell(row=0, col=0)
print(maze.exit)          # Cell(row=14, col=19)
print(maze.forty_two)     # list[Cell] — cells forming the "42" pattern

### Solving the maze
from solver import bfs
path = bfs(maze.grid, (maze.entry, maze.exit))

# path is a list of (Cell, Direction) tuples describing the shortest route
for cell, direction in path:
    print(f"From {cell} go {direction}")

### Custom parameters
Parameter > Type > Description
`size` > `tuple[int, int]` > `(height, width)` of the maze
`entry_exit` > `tuple[Cell, Cell] > None` > Entry and exit cells; defaults to corners
`ft` > `bool` > Whether to embed the "42" pattern (default `True`)

The `MazeConfig` dataclass returned by `parse_config()` from `config_parser.py` gathers all settings in one place and is suitable for driving both generation and display.

## Resources
### Maze generation
- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Think Labyrinth: Maze algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Jamis Buck's blog — Maze algorithms](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### Python tools
- [curses — Python docs](https://docs.python.org/3/library/curses.html)
- [flake8](https://flake8.pycqa.org/)
- [mypy](https://mypy.readthedocs.io/)

### AI usage
Claude (Anthropic) was used to assist with the project:
All AI-generated content was reviewed, tested, and understood before inclusion. No generation or solving logic was produced by AI.

## Team and project management
### Roles
Member > Responsibilities
mmelo
    Maze generation (backtracking), `geneator_maze.py`, `grid.py`, `hex_helpers.py`, solver
olistoke
    Maze generation (Prim's), config parser, Makefile, README

### Planning
The project was planned in three phases:
1. **Core data structures** — `Cell`, `Grid`, `HexGrid`, wall encoding helpers.
2. **Generation and solving** — recursive backtracking, BFS solver, "42" pattern, imperfect mode.
3. **Display and wiring** — curses renderer, state machine, config parsing, output file.
The main deviation from the initial plan was extracting `config_parser.py` late in the project once the interface stabilised.

### What worked well
- The hexadecimal wall encoding kept the output format and the grid logic tightly aligned.
- The `Machine` / `State` pattern made adding new keyboard interactions straightforward.
- Keeping generation (`Maze`) fully decoupled from display (`MazePrint`) made both easier to test.

### What could be improved
- The typo in `geneator_maze.py` (missing `r`) should be fixed and imports updated.
- More generation algorithms (Prim's, Kruskal's) could be added as a bonus.
- Unit tests with `pytest` would improve confidence during refactoring.

### Tools used
- **VS Code** with the Pylance extension for type checking during development.
- **mypy** and **flake8** for static analysis.
