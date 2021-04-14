"""
board.py:
Contains the Board class, which contains information about the board (size, game pieces).
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

from typing import List, Tuple, Set


class Board:
    """
    Board class, contains information about the board, such as board size and game pieces.
    Also has methods to clear board, etc.

    Instance Attributes:
     - size: Size of the board (in squares). Defaulted to 8.
     - pieces: A two-dimensional <size> by <size> array containing the board's pieces represented
               by integers: 0 denotes empty piece, 1 denotes black, and -1 denotes white.
               Accessed by pieces[row][column] (i.e. pieces[y][x])
     - next_moves: A set containing (int, int) tuples of square positions that are possible
                   next moves for the player
    """

    size: int
    pieces: List[List[int]]
    next_moves: Set[Tuple[int, int]]

    # Private Instance Attributes:
    # - _next_size: What size to set the board to next time the board is created. This is
    #               used so the board does not change size in the middle of a game if
    #               self.set_size is called, and so the board size only changes when
    #               self.create_board is called.

    _next_size = 8

    def __init__(self) -> None:
        """Initialize the board."""

        self.pieces = []
        self.next_moves = set()

        self.create_board()

    def set_size(self, size: int) -> None:
        """Set the size of the board."""
        self._next_size = size

    def set_piece(self, row: int, column: int, type: int) -> None:
        """Set the type of the piece at [row][column] to <type>.
        type is 0 if empty, 1 if black, -1 if white.

        If the [row][column] is out of bounds, raise IndexError.
        If type is not in {-1, 0, 1}, raise ValueError
        """
        if row >= self.size or column >= self.size:
            raise IndexError
        elif type not in {-1, 0, 1}:
            raise ValueError
        else:
            self.pieces[row][column] = type

    def get_piece(self, row: int, column: int) -> int:
        """Retrieve a piece at a row and column. Note that this indexes from 0.
        If the [row][column] is out of bounds, raise IndexError.
        """

        if row >= self.size or column >= self.size:
            raise IndexError
        else:
            return self.pieces[row][column]

    def is_next_move(self, row: int, column: int) -> bool:
        """Return whether or not the square at [row][column] is a possible next move for the
        next player.
        """
        return (row, column) in self.next_moves

    def set_next_move(self, row: int, column: int, allowed: bool) -> None:
        """Change whether or not the square at [row][column] is an allowed next move."""
        if not allowed:
            if (row, column) in self.next_moves:
                self.next_moves.remove((row, column))
        else:
            self.next_moves.add((row, column))

    def create_board(self) -> None:
        """Create a new board, update size and clear the board."""
        self.size = self._next_size

        self.clear_board()

    def clear_board(self) -> None:
        """Clear the board, creating a new 2-D <self.size> by <self.size> array
        filled with 0s."""

        self.pieces.clear()
        self.next_moves.clear()

        for row in range(self.size):
            self.pieces.append([0] * self.size)
