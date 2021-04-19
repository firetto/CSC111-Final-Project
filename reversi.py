"""
reversi.py
Contains the ReversiGame class, which represents a game state of a Reversi game.
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

from __future__ import annotations
import copy
from typing import Optional, Set, Tuple
from board import Board

_BLACK = 1
_WHITE = -1


class ReversiGame:
    """A class representing a state of a game of Reversi.

    >>> game = ReversiGame()
    >>> # Get all valid moves for black at the start of the game.
    >>> game.get_valid_moves() == {(2, 4), (3, 5), (4, 2), (5, 3)}
    True
    >>> game.make_move((2, 4))
    >>> game.get_valid_moves() == {(2,5), (4,5), (2,3)}
    True

    Private Instance Attributes:
    - _board: a Board instance representing the game board.
    - _current_player: an int representing the current player (1 for black, -1 for white)
    - _move_count: the number of moves that have been made in the current game
    - _human_player: int representing which player the human is (1 for black, -1 for white
                     and 0 if there is no human player in the game)
    """

    _board: Board
    _current_player: int
    _move_count: int
    _human_player: int

    def __init__(self, board: list[list[int]] = None,
                 current_player: int = _BLACK, move_count: int = 0, human_player: int = 0) -> None:
        """Initializer for ReversiGame.

        Preconditions:
        - board is a square 2-d list
        - current_player in [_BLACK, _WHITE]
        - move_count >= 0
        - human_player in [_BLACK, _WHITE, 0]
        """

        self._board = Board()

        self.start_game(board, current_player, move_count, human_player)

    def start_game(self, board: list[list[int]] = None, current_player: int = _BLACK,
                   move_count: int = 0, human_player: int = 0) -> None:
        """Reinitialize the board, set attributes.

        Preconditions:
        - board is a square 2-d list
        - current_player in [_BLACK, _WHITE]
        - move_count >= 0
        - human_player in [_BLACK, _WHITE, 0]
        """

        if board is not None:
            self._board.set_board(board)
        else:
            self._board.create_board()
            self._board.set_piece(row=self._board.size // 2 - 1, column=self._board.size // 2 - 1,
                                  piece_type=1)
            self._board.set_piece(row=self._board.size // 2 - 1, column=self._board.size // 2,
                                  piece_type=-1)
            self._board.set_piece(row=self._board.size // 2, column=self._board.size // 2 - 1,
                                  piece_type=-1)
            self._board.set_piece(row=self._board.size // 2, column=self._board.size // 2,
                                  piece_type=1)

        self._current_player = current_player
        self._move_count = move_count
        self._human_player = human_player

        self._recalculate_valid_moves()

    def get_board(self) -> Board:
        """Return the Board instance."""
        return self._board

    def set_board_size(self, size: int) -> None:
        """Set the board size to <size>.

        Preconditions:
         - size >= 2
         """
        self._board.set_size(size)

    def get_human_player(self) -> int:
        """Return the integer representing the human player"""
        return self._human_player

    def get_valid_moves(self) -> Set[Tuple[int, int]]:
        """Return a list of the valid moves for the active player."""
        return self._board.valid_moves

    def try_make_move(self, move: Tuple[int, int]) -> bool:
        """Try to make a Reversi move by calling make_move if the move is valid."""
        if self._board.is_valid_move(row=move[0], column=move[1]):
            self.make_move(move)
            return True
        return False

    def make_move(self, move: Tuple[int, int]) -> None:
        """Make the given Reversi move. This instance of a ReversiGame will be mutated, and will
        afterwards represent the game state after move is made.

        If move is not a currently valid move, raise a ValueError.
        """
        if not self._board.is_valid_move(row=move[0], column=move[1]):
            raise ValueError(f'Move "{move}" is not valid')

        self._board.set_board(self._board_after_move(move))
        self._current_player = -self._current_player
        self._move_count += 1
        self._recalculate_valid_moves()

    def copy_and_make_move(self, move: Tuple[int, int]) -> ReversiGame:
        """Make the given chess move in a copy of this ReversiGame, and return that copy.

        If move is not a currently valid move, raise a ValueError.
        """
        return ReversiGame(board=self._board_after_move(move),
                           current_player=-self._current_player,
                           move_count=self._move_count + 1)

    def get_current_player(self) -> int:
        """Return whether the black player is to move next."""
        return self._current_player

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.
        """
        if len(self._board.valid_moves) == 0:
            num_black = sum([row.count(1) for row in self._board.pieces])
            num_white = sum([row.count(-1) for row in self._board.pieces])
            if num_black > num_white:
                return 'black'
            elif num_black < num_white:
                return 'white'
            else:
                return 'draw'

        return None

    def _calculate_moves_and_paths_for_board(self, current_player: int) \
            -> Tuple[Set[Tuple[int, int]], Set[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """Return all possible moves and paths on a given board with a given active player.
           A path is a tuple of two integers representing the start square and end square
           of the path of the pieces which will be changed to the current player's colour when
           the move is made.

        Preconditions:
        - current_player in [_BLACK, _WHITE]
        """
        moves_and_paths = (set(), set())

        for pos in [(row, col) for row in range(0, self._board.size)
                    for col in range(0, self._board.size)]:
            piece = self._board.get_piece(row=pos[0], column=pos[1])
            if piece in (-current_player, 0):
                continue

            current_p = current_player

            for direction in {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}:
                self._find_moves_and_paths_in_direction(moves_and_paths, pos, current_p, direction)

        return moves_and_paths

    def _find_moves_and_paths_in_direction(self, moves_and_paths: Tuple[Set[Tuple[int, int]],
                                                                        Set[Tuple[
                                                                            Tuple[int, int], Tuple[
                                                                                int, int]]]],
                                           pos: Tuple[int, int],
                                           current_player: int, direction: Tuple[int, int]) -> None:
        """Find a valid move moving in a given direction from a certain position, and store
           the path from the start square to the square on which the move is executed.

        Preconditions:
        - current_player in [_BLACK, _WHITE]
        - direction in {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}
        """
        stop = False
        i = 1
        other_player = -current_player
        while not stop:
            row, col = pos[0] + direction[0] * i, pos[1] + direction[1] * i

            if row < 0 or col < 0 or row >= self._board.size or col >= self._board.size:
                break  # Out of bounds
            # Break if there is another current_player piece in that direction or the first
            # space in that direction is empty
            if self._board.get_piece(row=row, column=col) == current_player or \
                    (self._board.get_piece(row=row, column=col) == 0
                     and (row, col) == (pos[0] + direction[0], pos[1] + direction[1])):
                break
            if self._board.get_piece(row=row, column=col) == other_player:
                pass
            # We have passed at least one of other_player pieces and reached an empty space
            else:
                moves_and_paths[0].add((row, col))
                moves_and_paths[1].add(((pos[0], pos[1]), (row, col)))
                break

            i += 1

    def _board_after_move(self, move: Tuple[int, int]) -> list[list[int]]:
        """Return a copy of self._board.pieces representing the state of
        the board after making move.

        Precondition:
        x in list(range(self._board.size)) for x in move
        """

        paths = self._calculate_moves_and_paths_for_board(self.get_current_player())[1]
        filter_paths = {p for p in paths if p[1] == move}
        board_copy = copy.deepcopy(self._board.pieces)
        board_copy[move[0]][move[1]] = self.get_current_player()
        for path in filter_paths:
            direction = get_direction(path[0], path[1])
            piece_x = path[0][0] + direction[0]
            piece_y = path[0][1] + direction[1]
            while (piece_x, piece_y) != path[1]:
                board_copy[piece_x][piece_y] = self.get_current_player()
                piece_x += direction[0]
                piece_y += direction[1]

        return board_copy

    def _recalculate_valid_moves(self) -> None:
        """Update the valid moves for this game board."""

        self._board.valid_moves = self._calculate_moves_and_paths_for_board(
            self.get_current_player())[0]


def get_direction(v1: Tuple[int, int], v2: Tuple[int, int]) -> list[int, int]:
    """Get tuple representing direction vector between v1 and v2"""
    direction = [0, 0]
    for i in range(2):
        if v2[i] - v1[i] == 0:
            pass
        else:
            direction[i] = int((v2[i] - v1[i]) / abs(v2[i] - v1[i]))
    return direction


if __name__ == "__main__":
    # Test doctests
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['copy', 'time', 'board'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,

        # Disable too-many-nested-blocks, too-many-arguments
        'disable': ['E1136', 'R1702', 'R0913']
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
