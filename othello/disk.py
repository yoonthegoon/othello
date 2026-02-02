from typing import Self

from othello._typing import Side


class Disk:
    def __init__(self, side: Side) -> None:
        self.side = side

    def __repr__(self) -> str:
        return f"Disk(side={self.side})"

    def flip(self) -> Self:
        match self.side:
            case Side.DARK:
                self.side = Side.LIGHT
            case Side.LIGHT:
                self.side = Side.DARK
        return self
