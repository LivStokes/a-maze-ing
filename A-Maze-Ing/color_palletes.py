from dataclasses import dataclass
from itertools import cycle
import curses
from typing import Literal

value = Literal[0,1,2,3,4,5]

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

    @staticmethod
    def rgb_to_code(red: value, green: value, blue: value) -> int:
        return 16 + (red * 36) + (green * 6) + blue

    @staticmethod
    def lighter_color(rgb: tuple[value,value,value]) -> tuple[value,value,value]:
        return tuple((val - 1 if val != 0 else 0 for val in rgb))

    def new_color_pallete(self, red: value, green: value, blue: value):
        colors: list[tuple[value,value,value]] = [(red, green, blue)]
        for _ in range(5):
            colors.append(self.lighter_color(colors[-1]))
        colors8bit: list[int] = [self.rgb_to_code(*color) for color in colors]
        self.new_pallete(self.get(colors8bit[4], colors8bit[1]),
                         self.get(colors8bit[0]),
                         self.get(colors8bit[5]),
                         self.get(colors8bit[3]),
                         self.get(colors8bit[3]))

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
#colors.new_pallete(colors.get(237, 250),
#                   colors.get(255),
#                   colors.get(233),
#                   colors.get(243),
#                   colors.get(240))
#colors.new_color_pallete(4,5,5)
#colors.new_color_pallete(5,4,5)
#colors.new_color_pallete(5,5,4)
#colors.new_color_pallete(5,4,4)
#colors.new_color_pallete(4,4,5)
#colors.new_color_pallete(4,5,4)
#colors.new_color_pallete(5,4,0)
#colors.new_color_pallete(0,4,5)
#colors.new_color_pallete(5,2,4)
#colors.new_color_pallete(2,5,3)
#colors.new_color_pallete(4,1,3)
#colors.next_pallete()
