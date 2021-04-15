"""
ai_players.py:
Contains the  pieces).
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""
from reversi import ReversiGame
import random
from game_tree import GameTree
from typing import Optional


def example_heuristic(game: ReversiGame) -> float:
    return 0.0


class Player:
    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        raise NotImplementedError


class RandomPlayer(Player):
    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        return random.choice(list(game.get_valid_moves()))


class GreedyPlayer(Player):
    _tree: Optional[GameTree]
    depth: int
    heuristic: callable

    def __init__(self, depth: int):
        self.depth = depth
        self._tree = self._create_tree((-1, -1), ReversiGame(), depth)

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        self._tree = self._tree.find_subtree_by_move(previous_move)
        if self._tree is None:
            self._tree = self._create_tree((-1, -1), game, self.depth)
        else:
            self._update_tree(game, self._tree)
        subtrees = self._tree.get_subtrees()
        self._tree = max(subtrees, key=lambda x: x.evaluation)
        return self._tree.move

    def _create_tree(self, root_move: tuple[int, int], game: ReversiGame, depth: float) -> GameTree:
        color = game.get_current_player() == 1
        ret = GameTree(move=root_move, is_white_move=color)
        possible_moves = game.get_valid_moves()
        for move in possible_moves:
            new_game = game.copy_and_make_move(move)
            evaluation = example_heuristic(new_game)
            if depth != 1:
                new_subtree = self._create_tree(move, new_game, depth - 1)
            else:
                new_subtree = GameTree(move=move, is_white_move=not color)
            new_subtree.evaluation = evaluation
            ret.add_subtree(new_subtree)
        return ret

    def _update_tree(self, game: ReversiGame, tree: GameTree) -> None:
        possible_moves = game.get_valid_moves()
        if tree.get_subtrees() is None:
            for move in possible_moves:
                new_game = game.copy_and_make_move(move)
                evaluation = example_heuristic(new_game)
                new_tree = GameTree(evaluation, move, not tree.is_white_move)
                tree.add_subtree(new_tree)
        else:
            for subtree in tree.get_subtrees():
                self._update_tree(game, subtree)
