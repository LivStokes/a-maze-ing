from dataclasses import dataclass
from itertools import cycle
import curses

@dataclass(frozen=True)
class ColorPalette:
    walls: int
    entry: int
    exit: int
    path: int
    forty_two: int

class ColorManager:
    def __init__(self):
        self._palletes: list[ColorPalette] = []
        self._pairs: dict[tuple[int, int], int] = {}
        self._pair_ID: int = 1

    def get(self, fg: int, bg: int =-1):
        key = (fg, bg)
        if key not in self._pairs:
            curses.init_pair(self._pair_ID, fg, bg)
            self._pairs[key] = self._pair_ID
            self._pair_ID += 1
        return curses.color_pair(self._pairs[key])
    
    def new_pallete(self, walls: int, entry: int, exit: int, path: int,
                    forty_two: int):
        self._palletes.append(ColorPalette(walls, entry, exit, path, forty_two))
        self._pallete_cycler = cycle(self._palletes)

    def next_pallete(self) -> ColorPalette:
        self.pallete: ColorPalette = next(self._pallete_cycler)
        return self.pallete

colors = ColorManager()
curses.use_default_colors()
colors.new_pallete(colors.get(curses.COLOR_BLACK, curses.COLOR_WHITE),
                    colors.get(curses.COLOR_GREEN),
                    colors.get(curses.COLOR_RED),
                    colors.get(curses.COLOR_BLUE),
                    colors.get(curses.COLOR_YELLOW))
colors.new_pallete(colors.get(curses.COLOR_RED, curses.COLOR_CYAN),
                    colors.get(curses.COLOR_GREEN),
                    colors.get(curses.COLOR_WHITE),
                    colors.get(curses.COLOR_BLUE),
                    colors.get(curses.COLOR_YELLOW))
colors.next_pallete()