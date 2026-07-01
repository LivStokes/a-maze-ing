from dataclasses import dataclass
from itertools import cycle
import curses
from typing import cast


@dataclass(frozen=True)
class ColorPalette:
    """An immutable container for curses color pair IDs representing different
    maze components."""
    walls: int
    entry: int
    exit: int
    path: int
    forty_two: int


class ColorManager:
    """Manages dynamic creation, caching, and cycling of curses color pairs
    and palettes."""
    def __init__(self) -> None:
        """Initialize the color manager with empty collections for palettes
        and color pair mappings."""
        self._palletes: list[ColorPalette] = []
        self._pairs: dict[tuple[int, int], int] = {}
        self._pair_ID: int = 1

    def get(self, fg: int, bg: int = -1) -> int:
        key = (fg, bg)
        if key not in self._pairs:
            curses.init_pair(self._pair_ID, fg, bg)
            self._pairs[key] = self._pair_ID
            self._pair_ID += 1
        return curses.color_pair(self._pairs[key])

    def new_pallete(self, walls: int, entry: int, exit: int, path: int,
                    forty_two: int) -> None:
        """Append a new ColorPalette to the manager and reset the cycling
        iterator."""
        self._palletes.append(ColorPalette(walls, entry, exit, path,
                                           forty_two))
        self._pallete_cycler = cycle(self._palletes)

    def next_pallete(self) -> ColorPalette:
        """Advance to and return the next ColorPalette in the cyclic
        rotation."""
        self.pallete: ColorPalette = next(self._pallete_cycler)
        return self.pallete

    @staticmethod
    def rgb_to_code(red: int, green: int, blue: int) -> int:
        """Convert 6x6x6 RGB coordinate values into a standard 256-color
        xterm terminal code."""
        return 16 + (red * 36) + (green * 6) + blue

    @staticmethod
    def lighter_color(rgb: tuple[int, int,
                                 int]) -> tuple[int, int, int]:
        """Decrease RGB component intensities by 1 to generate a darker
        variant of the given color."""
        return cast(tuple[int, int, int],
                    tuple((val - 1 if val != 0 else 0 for val in rgb)))

    def new_color_pallete(self, red: int, green: int, blue: int) -> None:
        """Generate a gradient of terminal colors from a base RGB value and
        register it as a new palette."""
        colors: list[tuple[int, int, int]] = [(red, green, blue)]
        for _ in range(5):
            colors.append(self.lighter_color(colors[-1]))
        colors8bit: list[int] = [self.rgb_to_code(*color) for color in colors]
        self.new_pallete(self.get(colors8bit[4], colors8bit[1]),
                         self.get(colors8bit[0]),
                         self.get(colors8bit[5]),
                         self.get(colors8bit[3]),
                         self.get(colors8bit[3]))


COLORS = ColorManager()
curses.use_default_colors()
COLORS.new_pallete(COLORS.get(curses.COLOR_BLACK, curses.COLOR_WHITE),
                   COLORS.get(curses.COLOR_GREEN),
                   COLORS.get(curses.COLOR_RED),
                   COLORS.get(curses.COLOR_BLUE),
                   COLORS.get(curses.COLOR_YELLOW))
COLORS.new_pallete(COLORS.get(curses.COLOR_RED, curses.COLOR_CYAN),
                   COLORS.get(curses.COLOR_GREEN),
                   COLORS.get(curses.COLOR_WHITE),
                   COLORS.get(curses.COLOR_BLUE),
                   COLORS.get(curses.COLOR_YELLOW))
if curses.COLORS >= 256:
    COLORS.new_pallete(COLORS.get(237, 250),
                       COLORS.get(255),
                       COLORS.get(233),
                       COLORS.get(243),
                       COLORS.get(240))
    COLORS.new_color_pallete(4, 5, 5)
    COLORS.new_color_pallete(5, 4, 5)
    COLORS.new_color_pallete(5, 5, 4)
    COLORS.new_color_pallete(5, 4, 4)
    COLORS.new_color_pallete(4, 4, 5)
    COLORS.new_color_pallete(4, 5, 4)
    COLORS.new_color_pallete(5, 4, 0)
    COLORS.new_color_pallete(0, 4, 5)
    COLORS.new_color_pallete(5, 2, 4)
    COLORS.new_color_pallete(2, 5, 3)
    COLORS.new_color_pallete(4, 1, 3)
COLORS.next_pallete()
