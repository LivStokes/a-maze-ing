from __future__ import annotations
from typing import Literal
from enum import IntEnum

HexChar = Literal['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                    'B', 'C', 'D', 'E', 'F']

HexDigit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3


    def __str__(self) -> str:
        return {
            Direction.N: 'N',
            Direction.S: 'S',
            Direction.E: 'E',
            Direction.W: 'W'
        }[self]

    def __repr__(self) -> str:
        return {
            Direction.N: 'N',
            Direction.S: 'S',
            Direction.E: 'E',
            Direction.W: 'W'
        }[self]

    @property
    def opposite(self) -> Direction:
        return {
            Direction.N: Direction.S,
            Direction.S: Direction.N,
            Direction.E: Direction.W,
            Direction.W: Direction.E,
        }[self]

    @property
    def uni_vector(self) -> tuple[int, int]:
        return {
            Direction.N: (-1, 0),
            Direction.S: (1, 0),
            Direction.E: (0, 1),
            Direction.W: (0, -1),
        }[self]

def validate_hex(value: int) -> None:
    if not (0 <= value <= 15):
        raise ValueError("Not a valid hex digit")


def hex_break(hex1: HexDigit, hex2: HexDigit,
                dir: Direction) -> tuple[HexDigit, HexDigit]:
    hex1 &= ~(1 << dir)
    hex2 &= ~(1 << dir.opposite)
    return hex1, hex2


def hex_build(hex1: HexDigit, hex2: HexDigit,
                dir: Direction) -> tuple[HexDigit, HexDigit]:
    hex1 |= (1 << dir)
    hex2 |= (1 << dir.opposite)
    return hex1, hex2


def hex_flip(hex1: HexDigit, hex2: HexDigit,
                dir: Direction) -> tuple[HexDigit, HexDigit]:
    hex1 ^= (1 << dir)
    hex2 ^= (1 << dir.opposite)
    return hex1, hex2


def is_wall(hex: HexDigit, dir: Direction) -> bool:
    return bool(1 & (hex >> dir))