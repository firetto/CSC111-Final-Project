"""
ai_players.py:
Contains the  pieces).
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""
from reversi import ReversiGame
import random
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
    this is an example of a heuristic function. this function returns the difference between the number of
    white and black pieces. if one side wins in a position, it gets assigned a value of 100000/-100000
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
        if white - black < -400:
            print(pieces)
            print(heuristic_array)
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
    """

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        """
        make_move is a function that takes a game position and the previous move in the game and returns
        a valid move
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """
    RandomPlayer is a player that plays random moves
    """

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        return random.choice(list(game.get_valid_moves()))


class MinimaxPlayer(Player):
    """
    MinimaxPlayer is a player that uses the minimax algorithm to calculate the next move

    Instance Attributes:
     - depth: the depth that the player will calculate to when making a decision
     - heuristic_array: array that dictates how the board is evaluated
    """
    depth: int
    heuristic_array: list[list[int]]

    def __init__(self, depth: int, heuristic_array: list[list[int]]):
        self.depth = depth
        self.heuristic_array = heuristic_array

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        tree = self._create_tree(previous_move, game, 0)
        print(tree)
        subtrees = tree.get_subtrees()
        # if the tree is white's move, then it is currently black's turn, as the root holds the previous move
        if not tree.is_white_move:
            best_tree = max(subtrees, key=lambda x: x.evaluation)
        else:
            best_tree = min(subtrees, key=lambda x: x.evaluation)
        return best_tree.move

    def _create_tree(self, root_move: tuple[int, int], game: ReversiGame, depth: int) -> GameTree:
        # the root_move is one move behind the game, thus if the game is at white's turn, then the root happened
        # on black's turn. 1 represents black's turn, -1 represents white's turn
        color = (game.get_current_player() == 1)
        ret = GameTree(move=root_move, is_white_move=color)
        if depth == self.depth:
            ret.evaluation = heuristic(game, self.heuristic_array)
            return ret
        possible_moves = list(game.get_valid_moves())
        # shuffle for randomness
        random.shuffle(possible_moves)
        for move in possible_moves:
            new_game = game.copy_and_make_move(move)
            new_subtree = self._create_tree(move, new_game, depth + 1)
            ret.add_subtree(new_subtree)
        # update the evaluation value of the tree once all subtrees are added
        ret.update_evaluation()
        return ret


class MinimaxABPlayer(Player):
    depth: int
    heuristic_array: list[list[int]]

    def make_move(self, game: ReversiGame, previous_move: tuple[int, int]):
        return

    def _minimax(self, root_move: tuple[int, int], depth: int, game: ReversiGame,
                 alpha: float, beta: float) -> GameTree:
        color = (game.get_current_player() == 1)
        ret = GameTree(move=root_move, is_white_move=color)
        if depth == self.depth:
            ret.evaluation = 0


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
            white += 1
        elif game.get_winner() == 'black':
            black += 1
        else:
            ties += 1
    print("Player 1 Wins: " + str(black))
    print("Player 2 Wins: " + str(white))
