"""
reversi.py
Contains the ReversiGame class, which represents a game state of a Reversi game.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

from __future__ import annotations
import copy
from typing import Optional, Set, Tuple


class ReversiGame:
    """A class representing a state of a game of Reversi.

    >>> game = ReversiGame()
    >>> # Get all valid moves for black at the start of the game.
    >>> game.get_valid_moves() == {(2, 4), (3, 5), (4, 2), (5, 3)}
    True
    >>> game.make_move((2, 4))
    >>> game.get_valid_moves() == {(2,5), (4,5), (2,3)}
    True

    # >>> # If you try to make an invalid move, a ValueError is raised.
    # >>> game.make_move('a4d1')
    # Traceback (most recent call last):
    # ValueError: Move "a4d1" is not valid
    # >>> # This move is okay.
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional representation of a Reversi board
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _current_player: an int representing the current player (1 for black, -1 for white)
    #   - _move_count: the number of moves that have been made in the current game
    _board: list[list[int]]
    _valid_moves: Set[Tuple[int, int]]
    _current_player: int
    _move_count: int

    def __init__(self, board: list[list[int]] = None,
                 current_player: int = 1, move_count: int = 0) -> None:

        if board is not None:
            self._board = board
        else:
            self._board = [[0 for _ in range(8)] for _ in range(3)] + [[0, 0, 0, 1, -1, 0, 0, 0]] \
                          + [[0, 0, 0, -1, 1, 0, 0, 0]] + [[0 for _ in range(8)] for _ in range(3)]

        self._current_player = current_player
        self._move_count = move_count
        self._valid_moves = set()

        self._recalculate_valid_moves()

    def get_valid_moves(self) -> Set[Tuple[int, int]]:
        """Return a list of the valid moves for the active player."""
        return self._valid_moves

    def make_move(self, move: Tuple[int, int]) -> None:
        """Make the given Reversi move. This instance of a ReversiGame will be mutated, and will
        afterwards represent the game state after move is made.

        If move is not a currently valid move, raise a ValueError.
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is not valid')

        self._board = self._board_after_move(move)

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
        if len(self._valid_moves) == 0:
            num_black = sum([row.count(1) for row in self._board])
            num_white = sum([row.count(-1) for row in self._board])
            if num_black > num_white:
                return 'black'
            elif num_black < num_white:
                return 'white'
            else:
                return 'draw'

    def _calculate_moves_and_paths_for_board(self,
                                             current_player: int) \
            -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int], Tuple[int, int]]]:
        """Return all possible moves and paths on a given board with a given active player.
           A path is a tuple of two integers representing the start square and end square
           of the path of the pieces which will be changed to the current player's colour when
           the move is made.
        """
        moves_and_paths = (set(), set())

        for pos in [(x, y) for x in range(0, 8) for y in range(0, 8)]:
            piece = self._board[pos[0]][pos[1]]
            if piece == -current_player or piece == 0:
                continue

            current_p = current_player

            for dir in {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}:
                self._find_moves_and_paths_in_direction(moves_and_paths, pos, current_p, dir)

        return moves_and_paths

    def _find_moves_and_paths_in_direction(self, moves_and_paths: Tuple[
        Set[Tuple[int, int]], Set[Tuple[int, int], Tuple[int, int]]], pos: Tuple[int, int],
                                           current_player: int, direction: Tuple[int, int]):
        """Find a valid move moving in a given direction from a certain position, and store
           the path from the start square to the square on which the move is executed.
        """
        stop = False
        i = 1
        other_player = -current_player

        while not stop:
            x, y = pos[0] + direction[0] * i, pos[1] + direction[1] * i

            if x < 0 or y < 0 or x > 7 or y > 7:
                break  # Out of bounds
            # Break if there is another current_player piece in that direction or the first
            # space in that direction is empty
            if self._board[x][y] == current_player or \
                    (self._board[x][y] == 0 and (x, y) == (
                            pos[0] + direction[0], pos[1] + direction[1])):
                break
            if self._board[x][y] == other_player:
                pass
            # We have passed at least one of other_player pieces and reached an empty space
            else:
                moves_and_paths[0].add((x, y))
                moves_and_paths[1].add(((pos[0], pos[1]), (x, y)))
                break

            i += 1

    def _board_after_move(self, move: Tuple[int, int]) -> list[list[int]]:
        """Return a copy of self._board representing the state of the board after making move.
        """
        paths = self._calculate_moves_and_paths_for_board(self.get_current_player())[1]
        filter_paths = {path for path in paths if path[1] == move}
        board_copy = copy.deepcopy(self._board)
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

        self._valid_moves = self._calculate_moves_and_paths_for_board(self.get_current_player())[0]


def get_direction(v1: Tuple[int, int], v2: Tuple[int, int]) -> list[int, int]:
    """Get tuple representing direction vector between v1 and v2"""
    direction = [0, 0]
    for i in range(2):
        if v2[i] - v1[i] == 0:
            pass
        else:
            direction[i] = int((v2[i] - v1[i]) / abs(v2[i] - v1[i]))
    return direction


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
