"""Module defining Direction, hex digit types, and bitwise wall manipulation
utilities."""
from __future__ import annotations
from typing import Literal, cast
from enum import IntEnum

HexChar = Literal['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A',
                  'B', 'C', 'D', 'E', 'F']

HexDigit = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


class Direction(IntEnum):
    """Cardinal direction enum used to navigate and manipulate maze cell
    walls."""
    N = 0
    E = 1
    S = 2
    W = 3

    def __str__(self) -> str:
        """Return the single-character string name of the direction."""
        return {
            Direction.N: 'N',
            Direction.S: 'S',
            Direction.E: 'E',
            Direction.W: 'W'
        }[self]

    def __repr__(self) -> str:
        """Return the single-character string representation of the
        direction."""
        return {
            Direction.N: 'N',
            Direction.S: 'S',
            Direction.E: 'E',
            Direction.W: 'W'
        }[self]

    @property
    def opposite(self) -> Direction:
        """Return the direction directly opposite to this one."""
        return {
            Direction.N: Direction.S,
            Direction.S: Direction.N,
            Direction.E: Direction.W,
            Direction.W: Direction.E,
        }[self]

    @property
    def uni_vector(self) -> tuple[int, int]:
        """Return the unit vector for this direction as a (row, col) tuple."""
        return {
            Direction.N: (-1, 0),
            Direction.S: (1, 0),
            Direction.E: (0, 1),
            Direction.W: (0, -1),
        }[self]


def validate_hex(value: int) -> None:
    """Raise ValueError if the value is not a valid hex digit between 0 and
    15."""
    if not (0 <= value <= 15):
        raise ValueError("Not a valid hex digit")


def hex_break(hex1: HexDigit, hex2: HexDigit,
              dir: Direction) -> tuple[HexDigit, HexDigit]:
    """Clear the wall bit in both cells for the given direction, effectively
    removing the wall."""
    hex1 = cast(HexDigit, hex1 & ~(1 << dir))
    hex2 = cast(HexDigit, hex2 & ~(1 << dir.opposite))
    return hex1, hex2


def hex_build(hex1: HexDigit, hex2: HexDigit,
              dir: Direction) -> tuple[HexDigit, HexDigit]:
    """Set the wall bit in both cells for the given direction, effectively
    adding the wall."""
    hex1 = cast(HexDigit, hex1 | (1 << dir))
    hex2 = cast(HexDigit, hex2 | (1 << dir.opposite))
    return hex1, hex2


def hex_flip(hex1: HexDigit, hex2: HexDigit,
             dir: Direction) -> tuple[HexDigit, HexDigit]:
    """Toggle the wall bit in both cells for the given direction."""
    hex1 = cast(HexDigit, hex1 ^ (1 << dir))
    hex2 = cast(HexDigit, hex2 ^ (1 << dir.opposite))
    return hex1, hex2


def is_wall(hex: HexDigit, dir: Direction) -> bool:
    """Return True if the wall bit is set for the given direction in the hex
    digit."""
    return bool(1 & (hex >> dir))
