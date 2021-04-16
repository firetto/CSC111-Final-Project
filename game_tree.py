"""
game_tree.py:
Contains the game tree class
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

from __future__ import annotations


class GameTree:
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
        return self._subtrees

    def add_subtree(self, subtree: GameTree) -> None:
        self._subtrees.append(subtree)
        self.update_evaluation()

    def find_subtree_by_move(self, move: tuple[int, int]):
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree
        return None

    def update_evaluation(self):
        if self.is_white_move:
            for tree in self._subtrees:
                self.evaluation = max(tree.evaluation, self.evaluation)
        else:
            for tree in self._subtrees:
                self.evaluation = min(tree.evaluation, self.evaluation)

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
