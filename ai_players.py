"""
ai_players.py:
Contains the  pieces).
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

import time
import random
from reversi import ReversiGame
from game_tree import GameTree


POSITIONAL_HEURISTIC = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
]


def basic_heuristic(size: int) -> list[list[int]]:
    """
    function that returns a <size> by <size> array of ones
    """
    ret = []
    for _ in range(size):
        ret.append([1] * size)
    return ret


def heuristic(game: ReversiGame, heuristic_array: list[list[int]]) -> float:
    """
    this is an example of a heuristic function. this function returns
    the difference between the number of
    white and black pieces. if one side wins in a position, it gets
    assigned a value of 100000/-100000
    """

    if game.get_winner() is None:
        pieces = game.get_board().pieces
        black = 0
        white = 0
        length = len(pieces)
        for i in range(length):
            for m in range(length):
                if pieces[i][m] == 1:
                    black += heuristic_array[i][m]
                elif pieces[i][m] == -1:
                    white += heuristic_array[i][m]
        return white - black
    elif game.get_winner() == 'white':
        return 100000
    elif game.get_winner() == 'black':
        return -100000
    else:
        return 0


class Player:
    """
    Player is an abstract class that represents a reversi player

    Instance Attributes:
        - heuristic_array: array that dictates how the board is evaluated, used in
                           MinimaxPlayer and MinimaxABPlayer
    """

    heuristic_array: list[list[int]]

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        """
        make_move is a function that takes a game position and the previous
        move in the game and returns a valid move
        """
        raise NotImplementedError

    def set_heuristic(self, size: int) -> None:
        """Set the heuristic array BASED on board size. 8x8 will choose the POSITIONAL_HEURISTIC,
        while any other size will choose the basic_heuristic. (get it? I said based)"""

        if size == 8:
            self.heuristic_array = POSITIONAL_HEURISTIC
        else:
            self.heuristic_array = basic_heuristic(size)


class RandomPlayer(Player):
    """
    RandomPlayer is a player that plays random moves.
    """
    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        """Make a random move."""
        return random.choice(list(game.get_valid_moves()))


class MinimaxPlayer(Player):
    """
    MinimaxPlayer is a player that uses the minimax algorithm to calculate the next move

    Instance Attributes:
     - depth: the depth that the player will calculate to when making a decision
    """
    depth: int

    def __init__(self, depth: int, board_size: int):
        self.depth = depth
        self.set_heuristic(board_size)

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        tree = self._minimax(previous_move, game, 0)
        subtrees = tree.get_subtrees()
        # maximize if white's turn, else minimize
        if tree.is_white_move:
            best_tree = max(subtrees, key=lambda x: x.evaluation)
        else:
            best_tree = min(subtrees, key=lambda x: x.evaluation)
        return best_tree.move

    def _minimax(self, root_move: tuple[int, int], game: ReversiGame, depth: int) -> GameTree:
        """
        _minimax is a function that returns a tree where each node has a value determined by
        minimax search
        """
        white_move = (game.get_current_player() == -1)
        ret = GameTree(move=root_move, is_white_move=white_move)
        if depth == self.depth:
            ret.evaluation = heuristic(game, self.heuristic_array)
            return ret
        possible_moves = list(game.get_valid_moves())
        if not possible_moves:
            if game.get_winner() == 'white':
                ret.evaluation = 10000
            elif game.get_winner() == 'black':
                ret.evaluation = -10000
            else:
                ret.evaluation = 0
            return ret
        # shuffle for randomness
        random.shuffle(possible_moves)
        # best_value tracks the best possible move that the player can make
        best_value = float('-inf')
        if not white_move:
            best_value = float('inf')
        for move in possible_moves:
            new_game = game.copy_and_make_move(move)
            new_subtree = self._minimax(move, new_game, depth + 1)
            if white_move:
                best_value = max(best_value, new_subtree.evaluation)
            else:
                best_value = min(best_value, new_subtree.evaluation)
            ret.add_subtree(new_subtree)
        # update the evaluation value of the tree once all subtrees are added
        ret.evaluation = best_value
        return ret


class MinimaxABPlayer(Player):
    depth: int

    def __init__(self, depth: int, board_size: int):
        self.depth = depth
        self.set_heuristic(board_size)

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        tree = self._minimax(previous_move, 0, game, float('-inf'), float('inf'))
        subtrees = tree.get_subtrees()
        # if the tree is white's move, then it is currently black's turn,
        # as the root holds the previous move
        if tree.is_white_move:
            best_tree = max(subtrees, key=lambda x: x.evaluation)
        else:
            best_tree = min(subtrees, key=lambda x: x.evaluation)
        return best_tree.move

    def _minimax(self, root_move: tuple[int, int], depth: int, game: ReversiGame,
                 alpha: float, beta: float) -> GameTree:
        """
        _minimax is a minimax function with alpha-beta pruning implemented
        """
        # color represents if it is white's turn
        white_move = (game.get_current_player() == -1)
        ret = GameTree(move=root_move, is_white_move=white_move)
        if depth == self.depth:
            ret.evaluation = heuristic(game, self.heuristic_array)
            return ret
        possible_moves = list(game.get_valid_moves())
        if not possible_moves:
            if game.get_winner() == 'white':
                ret.evaluation = 10000
            elif game.get_winner() == 'black':
                ret.evaluation = -10000
            else:
                ret.evaluation = 0
            return ret
        random.shuffle(possible_moves)
        best_value = float('-inf')
        if not white_move:
            best_value = float('inf')
        for move in possible_moves:
            new_game = game.copy_and_make_move(move)
            new_tree = self._minimax(move, depth + 1, new_game, alpha, beta)
            ret.add_subtree(new_tree)
            # we update the alpha value when the maximizer is playing (white)
            if white_move and best_value < new_tree.evaluation:
                best_value = new_tree.evaluation
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            # we update the beta value when the minimizer is playing (black)
            elif not white_move and best_value > new_tree.evaluation:
                best_value = new_tree.evaluation
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
        ret.evaluation = best_value
        return ret


def test_players(player1: Player, player2: Player, iterations: int) -> None:
    """
    test_players is a function that runs <iterations> number of games between player1
    and player2
    """
    white = 0
    black = 0
    ties = 0
    for _ in range(iterations):
        game = ReversiGame()
        prev_move = (-1, -1)
        while game.get_winner() is None:
            move = player1.make_move(game, prev_move)
            game.try_make_move(move)
            if game.get_winner() is None:
                prev_move = player2.make_move(game, move)
                game.try_make_move(prev_move)
        if game.get_winner() == 'white':
            print('White WINS')
            white += 1
        elif game.get_winner() == 'black':
            print('Black WINS')
            black += 1
        else:
            print('TIE')
            ties += 1
    print("Player 1 Wins: " + str(black))
    print("Player 2 Wins: " + str(white))


def check_same(player1: Player, player2: Player) -> None:
    """
    check_same is a function that determines if two players return the same move throughout a game.
    this is particularly useful for comparison between MinimaxPlayer and MinimaxABPlayer.
    It also gives the time that each player takes to find a move.
    """
    game = ReversiGame()
    prev_move = (-1, -1)
    while game.get_winner() is None:
        start_time = time.time()
        print("Player 1 CHOOSING")
        move1 = player1.make_move(game, prev_move)
        print("--- %s seconds ---" % (time.time() - start_time))
        start_time = time.time()
        print("Player 2 CHOOSING")
        move2 = player2.make_move(game, prev_move)
        print("--- %s seconds ---" % (time.time() - start_time))
        print("Player 1 chose: ", move1, "  Player 2 chose: ", move2)
        assert move1 == move2
        game.try_make_move(move1)
        prev_move = move1
