from dataclasses import dataclass
from enum import Enum, auto
from typing import Annotated, Literal


class Direction(Enum):
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    EAST = (1, 0)
    SOUTHEAST = (1, 1)
    SOUTH = (0, 1)
    SOUTHWEST = (-1, 1)
    WEST = (-1, 0)
    NORTHWEST = (-1, -1)


class Player(Enum):
    DARK = auto()
    LIGHT = auto()


class State(Enum):
    NON_TERMINAL = auto()
    TERMINAL = auto()


@dataclass
class UnsignedInteger:
    bits: int


Passes = Literal[0, 1, 2]
Side = Player
Space = tuple[Annotated[int, UnsignedInteger(8)], Annotated[int, UnsignedInteger(8)]]
