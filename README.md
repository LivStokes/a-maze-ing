*This project has been created as part of the 42 curriculum by mmelo, olistoke.*

# Description
A-Maze-ing is a Python maze generator and visualiser.
Given a configuration file, it generates a maze of arbitrary size, optionally enforcing the *perfect maze* property (exactly one path between any two cells).
The maze is rendered interactively in the terminal using curses, and the output is written to a file using a hexadecimal wall encoding.
A hidden **"42"** pattern is embedded in every maze large enough to contain it.

# Instructions
### Requirements
- Python 3.10 or later
- A terminal that supports curses (standard on Linux/macOS)

### How to run
make install        # Create a virtual environment and install dev dependies.<br>
make rebuild        # Rebuilds the mazegen package from source
make run            # Run with the default config file.<br>
make debug          # Debug mode.<br>
make lint           # flake8 + mypy (standard flags).<br>
make lint-strict    # flake8 + mypy --strict.<br>
mkae clean          # Cleans excess files.<br>
python3 a_maze_ing.py my_config.txt

### Keyboard controls
Keys and their Actions:<br>
`g` = Re-generate a new maze<br>
`s` = Show / hide the shortest path<br>
`c` = Cycle through wall colour palettes<br>
`q` = Quit

### Configuration file
The config file uses one `KEY=VALUE` pair per line. 
Lines beginning with `#` are comments and are ignored. 
All keys are case-insensitive.

### Required keys
Key | Type | Description | Example<br>
`WIDTH` | positive int | Number of columns in the maze | `WIDTH=20`<br>
`HEIGHT` | positive int | Number of rows in the maze | `HEIGHT=15`<br>
`ENTRY` | positive ints | Entry cell coordinates (col, row) | `ENTRY=1,1`<br>
`EXIT` | positive ints | Exit cell coordinates (col, row) | `EXIT=19,14`<br>
`OUTPUT_FILE` | string | Path of the hex-encoded output file | `OUTPUT_FILE=maze.txt`<br>
`PERFECT` | bool | Enforce a single path between entry and exit | `PERFECT=True`

### Optional keys
Key | Type | Default | Description<br>
`SEED` | int | *(random)* | RNG seed for reproducible mazes<br>
`ALGORITHM` | string | `backtracking` | Generation algorithm (`backtracking`)<br>
`IMPERFECT_RATE` | float 0–1 | `0.1` | Probability of removing extra walls when `PERFECT=False`<br>

## Example config
### A-Maze-ing configuration
```
WIDTH=20
HEIGHT=15
ENTRY=1,1
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
ALGORITHM=backtracking
```

## Maze generation algorithms
### Backtracking
This project uses **recursive backtracking** which is also known as depth-first search maze generation.

### How it works
Starting from the entry cell, the algorithm visits unvisited neighbours in a random order, breaking the shared wall to connect them, and recurses into each. 
When no unvisited neighbours remain, it backtracks. The result is a *spanning tree* of the grid — a perfect maze.
If `PERFECT=False`, a post-processing pass randomly removes additional walls with probability `IMPERFECT_RATE`, creating loops and multiple paths.

### Why this algorithm?
- **Simplicity**: the recursive implementation maps cleanly onto the hexadecimal cell representation already used in this project.
- **Quality**: it produces mazes with long, winding corridors and few dead ends — visually interesting and challenging to solve.
- **Speed**: it runs in O(n) time and memory relative to the number of cells.
- **Reproducibility**: seeding Python's `random` module before generation makes any maze fully reproducible.

### Prim's
This project also uses Prim's algorithm, a minimum spanning tree method adapted for maze generation. 
Unlike backtracking which dives deep along a single path, Prim's grows the maze outward from a starting cell like an expanding frontier.

### How it works
A random cell is chosen and its unvisited neighbours are added to a frontier list. 
The algorithm repeatedly picks a random frontier cell, connects it to the visited maze by breaking the shared wall, 
and adds its own unvisited neighbours to the frontier — until every cell is visited.

### why this algorithm?
- **Different texture**: produces dense mazes with many short dead ends rather than long winding corridors.
- **Iterative**: the frontier-based approach avoids Python's recursion depth limits on large grids.
- **Reproducible**: seeding random before generation makes any maze fully reproducible.

## Output file format
Each cell is written as one uppercase hexadecimal digit encoding its four walls as bits:<br>
Bit | Direction<br>
0 (LSB) | North<br>
1 | East<br>
2 | South<br>
3 | West<br>
A bit of `1` means the wall is **closed**; `0` means **open**.<br>

Cells are written row by row, one row per line. After an empty line, three additional lines follow:<br>
1. Entry coordinates (`row,col`)
2. Exit coordinates (`row,col`)
3. Shortest path from entry to exit as a sequence of `N`, `E`, `S`, `W` characters.

All lines end with `\n`.

## Code reusability
The maze generation logic lives in `geneator_maze.py` as the `Maze` class. 
It is designed to be used independently of the display layer.
The core data structures — `Cell`, `Grid`, `HexGrid`, and `Maze` — live in `mazegen.utils.grid`, with the `Direction` enum and wall bit helpers in `mazegen.utils.hex_helpers`.
Maze generation is handled separately by the `Generator` abstract base class and its `BacktrackingGenerator` / `PrimsGenerator` subclasses in `mazegen.algorithms.maze_generators`, each of which builds and owns its own `Maze` instance.
All of this is designed to be used independently of the display layer.

<u>Quick-start example:</u><br>
```
from mazegen.utils.grid import Cell
from mazegen.algorithms.maze_generators import BacktrackingGenerator
```

<u>Create a 20×15 maze with entry at top-left and exit at bottom-right:</u><br>
```
generator = BackTrackingGenerator(
    height=15, width=20,
    entry=Cell(0, 0), exit=Cell(14, 19),
    ft=True,
)
generator.generate()
```

<u>Optionally remove some walls to make it imperfect (10 % probability):</u><br>
```
generator.imperfect(likelyhood=0.1)
```

<u>Access the hex grid:</u><br>
```
print(generator.grid)          # HexGrid — one hex digit per cell
```

<u>Access metadata:</u><br>
```
print(generator.maze.entry)         # Cell(row=0, col=0)<br>
print(generator.maze.exit)          # Cell(row=14, col=19)<br>
print(generator.forty_two)     # list[Cell] — cells forming the "42" pattern
```

<u>Solving the maze:</u><br>
```
from mazegen.algorithms.solver import bfs
path = bfs(generator.maze)
for step in path:
    print(f"From {step.cell} go {step.direction}")
```
`path` is a list of `Path_bit` objects (each with a `.cell` and a `.direction`) describing the shortest route.

<u>Custom parameters:</u><br>
Parameter | Type | Description <br>
`height`, `width` | `int` | Dimensions of the maze <br>
`entry`, `exit` | `Cell` | Entry and exit cells (no default — both are required) <br>
`ft` | `bool` | Whether to embed the "42" pattern (default `True`)

<u>Loading a config file:</u><br>
```
from mazegen.parsing.config_parser import parse_config
config = parse_config("config.txt")   # -> MazeConfig
```

The `MazeConfig` dataclass returned by `parse_config()` from `config_parser.py` gathers all settings in one place and is suitable for driving both generation and display.

# Resources
### Maze generation
- [Maze generation algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Think Labyrinth: Maze algorithms](http://www.astrolog.org/labyrnth/algrithm.htm)
- [Jamis Buck's blog — Maze algorithms](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### Python tools
- [curses — Python docs](https://docs.python.org/3/library/curses.html)
- [flake8](https://flake8.pycqa.org/)
- [mypy](https://mypy.readthedocs.io/)

### AI usage
Claude (Anthropic) was used to assist with the project:<br>
All AI-generated content was reviewed, tested, and understood before inclusion. No generation or solving logic was produced by AI.

## Team and project management
### Roles
Member | Responsibilities<br>
**mmelo:** 
- Maze generation algorithm = backtracking
- `geneator_maze.py`
- `grid.py`
- `hex_helpers.py`
- solver

**olistoke:**
- Maze generation algorithm = Prim's
- Configuration parsing
- Writing Docstrings
- Makefile
- README

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
- More generation algorithms could be added.
- Better color sequnces.
- The over all structure and planning of the project.

### Tools used
- **VS Code** with the Pylance extension for type checking during development.
- **mypy** and **flake8** for static analysis.
