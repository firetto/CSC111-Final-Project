"""
board.py:
Contains the Board class, which contains information about the board (size, game pieces).
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim

Copyright 2021 Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
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
     - valid_moves: A set containing (int, int) tuples of square positions that are possible
                   next moves for the player
    """

    size: int
    pieces: List[List[int]]
    valid_moves: Set[Tuple[int, int]]

    # Private Instance Attributes:
    # - _next_size: What size to set the board to next time the board is created. This is
    #               used so the board does not change size in the middle of a game if
    #               self.set_size is called, and so the board size only changes when
    #               self.create_board is called.

    _next_size: int = 8

    def __init__(self) -> None:
        """Initialize the board."""

        self.pieces = []
        self.valid_moves = set()

        self.create_board()

    def set_size(self, size: int) -> None:
        """Set the size of the board."""
        self._next_size = size

    def set_piece(self, row: int, column: int, piece_type: int) -> None:
        """Set the type of the piece at [row][column] to <type>.
        type is 0 if empty, 1 if black, -1 if white.

        If the [row][column] is out of bounds, raise IndexError.
        If type is not in {-1, 0, 1}, raise ValueError
        """
        if row >= self.size or column >= self.size:
            raise IndexError
        elif piece_type not in {-1, 0, 1}:
            raise ValueError
        else:
            self.pieces[row][column] = piece_type

    def get_piece(self, row: int, column: int) -> int:
        """Retrieve a piece at a row and column. Note that this indexes from 0.
        If the [row][column] is out of bounds, raise IndexError.
        """

        if row >= self.size or column >= self.size:
            raise IndexError
        else:
            return self.pieces[row][column]

    def is_valid_move(self, row: int, column: int) -> bool:
        """Return whether or not the square at [row][column] is a possible next move for the
        next player.
        """
        return (row, column) in self.valid_moves

    def set_valid_move(self, row: int, column: int, allowed: bool) -> None:
        """Change whether or not the square at [row][column] is an allowed next move."""
        if not allowed:
            if (row, column) in self.valid_moves:
                self.valid_moves.remove((row, column))
        else:
            self.valid_moves.add((row, column))

    def clear_valid_moves(self) -> None:
        """Clear the set of possible next moves."""
        self.valid_moves.clear()

    def create_board(self) -> None:
        """Create a new board, update size and clear the board."""
        self.size = self._next_size

        self.clear_board()

    def clear_board(self) -> None:
        """Clear the board, creating a new 2-D <self.size> by <self.size> array
        filled with 0s."""

        self.pieces.clear()
        self.valid_moves.clear()

        for _ in range(self.size):
            self.pieces.append([0] * self.size)

    def set_board(self, board: List[List[int]]) -> None:
        """Set self.pieces to <board>.

        Preconditions:
         - board is a <self.size> by <self.size> 2-d array of integers in {-1, 0, 1}
        """

        self.pieces = board


if __name__ == "__main__":
    # Test doctests
    import doctest
    doctest.testmod()

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': [],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,

        # Disable too-many-nested-blocks, too-many-arguments
        'disable': ['E1136', 'R1702', 'R0913']
    })
