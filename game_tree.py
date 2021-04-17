"""
game_tree.py:
Contains the game tree class
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

from __future__ import annotations
from typing import Optional


class GameTree:
    """
    GameTree is a class representing the possible moves in a reversi game

    Instance Attributes:
     - is_white_move: boolean representing if it is white's turn after the move is played
     - move: a tuple containing the row and column of the current move
     - evaluation: a float representing the evaluation of the tree

     Private Instance Attributes:
     - _subtrees: an array of GameTree that represents all of the following possible moves after the current move
    """
    move: tuple[int, int]
    is_white_move: bool
    _subtrees: list[GameTree]
    evaluation: float

    def __init__(self, evaluation: float = 0.0, move: tuple = (-1, -1), is_white_move: bool = False):
        self.move = move
        self.is_white_move = is_white_move
        self._subtrees = []
        self.evaluation = evaluation

    def get_subtrees(self) -> list[GameTree]:
        """
        Returns a list of all the subtrees
        """
        return self._subtrees

    def add_subtree(self, subtree: GameTree) -> None:
        self._subtrees.append(subtree)

    def find_subtree_by_move(self, move: tuple[int, int]) -> Optional[GameTree]:
        """
        find_subtree_by_move returns the subtree of the tree that contains the given move.
        if the move is not found, it returns None
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree
        return None

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_white_move:
            turn_desc = "White's move"
        else:
            turn_desc = "Black's move"
        move_desc = f'{self.move} -> {turn_desc}, {self.evaluation}\n'
        s = '  ' * depth + move_desc
        if not self._subtrees:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s
