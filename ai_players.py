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
    depth: int
    heuristic: callable

    def __init__(self, depth: int):
        self.depth = depth

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        tree = self._create_tree((-1, -1), game, self.depth)
        subtrees = tree.get_subtrees()
        best_tree = max(subtrees, key=lambda x: x.evaluation)
        return best_tree.move

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