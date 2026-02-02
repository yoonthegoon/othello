from typing import Self, cast

from othello._typing import Direction, Passes, Player, Side, Space, State
from othello.disk import Disk
from othello.exceptions import GameOverError, IllegalSpaceError


class Board:
    def __init__(self) -> None:
        self.grid: list[list[Disk | None]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.grid[3][3] = Disk(Side.DARK)
        self.grid[3][4] = Disk(Side.LIGHT)
        self.grid[4][3] = Disk(Side.LIGHT)
        self.grid[4][4] = Disk(Side.DARK)
        self.passes: Passes = 0
        self.state: State = State.NON_TERMINAL
        self.to_play: Player = Player.DARK

    @property
    def disc_counts(self) -> tuple[int, int]:
        dark_pieces, light_pieces = 0, 0
        for row in self.grid:
            for disk in row:
                if disk is None:
                    continue
                match disk.side:
                    case Side.DARK:
                        dark_pieces += 1
                    case Side.LIGHT:
                        light_pieces += 1
        return dark_pieces, light_pieces

    @property
    def legal_spaces(self) -> list[Space]:
        if self.state == State.TERMINAL:
            return []

        legal_spaces: list[Space] = []
        for x in range(8):
            for y in range(8):
                space = (x, y)
                if self.is_legal(space):
                    legal_spaces.append(space)
        return legal_spaces

    @property
    def score(self) -> tuple[int, int] | None:
        dark_count, light_count = self.disc_counts
        match self.winner:
            case Player.DARK:
                return 64 - light_count, light_count
            case Player.LIGHT:
                return dark_count, 64 - light_count
        return None

    @property
    def winner(self) -> Player | None:
        if self.state == State.NON_TERMINAL:
            return None
        dark_count, light_count = self.disc_counts
        if dark_count > light_count:
            return Player.DARK
        elif dark_count < light_count:
            return Player.LIGHT
        return None

    def alternate_players(self) -> Self:
        match self.to_play:
            case Player.DARK:
                self.to_play = Player.LIGHT
            case Player.LIGHT:
                self.to_play = Player.DARK
        return self

    def get_chain(self, space: Space, direction: Direction) -> list[Space]:
        x, y = space
        dir_x, dir_y = cast(tuple[int, int], direction.value)
        cur_x, cur_y = x + dir_x, y + dir_y

        if not (0 <= cur_x < 8 and 0 <= cur_y < 8):
            return []
        disk = self.grid[cur_y][cur_x]
        if disk is None:
            return []
        if disk.side == self.to_play:
            return []

        chain: list[Space] = [(cur_x, cur_y)]
        cur_x += dir_x
        cur_y += dir_y

        while 0 <= cur_x < 8 and 0 <= cur_y < 8:
            disk = self.grid[cur_y][cur_x]
            if disk is None:
                return []
            if disk.side == self.to_play:
                return chain

            chain.append((cur_x, cur_y))
            cur_x += dir_x
            cur_y += dir_y

        return []

    def is_legal(self, space: Space) -> bool:
        if self.state == State.TERMINAL:
            return False

        x, y = space
        if self.grid[y][x] is not None:
            return False

        for direction in Direction:
            if self.get_chain(space, direction):
                return True

        return False

    def play(self, space: Space) -> Self:
        if self.state == State.TERMINAL:
            raise GameOverError()
        if not self.legal_spaces:
            self.alternate_players()
            self.passes += 1
            if self.passes == 2:
                self.state = State.TERMINAL
            return self
        if not self.is_legal(space):
            raise IllegalSpaceError(f"illegal space: {space}")

        x, y = space
        self.grid[y][x] = Disk(self.to_play)

        spaces: list[Space] = []
        for direction in Direction:
            spaces.extend(self.get_chain(space, direction))

        for i, j in spaces:
            disk: Disk = self.grid[j][i]  # ty:ignore[invalid-assignment]
            disk.flip()

        self.alternate_players()
        self.passes = 0
        return self
