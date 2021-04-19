"""
generate_stats.py:
Generates the statistics for multiple games between two players, with the types of players specified
by the inputs to generate_stats.
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

import ai_players
import reversi
import stats


def generate_stats(player1: ai_players.Player, player2: ai_players.Player, board_size: int,
                   iterations: int) -> None:
    """Generates the statistics for iterations number of games between player1 and player2. player1
    represents the black player and player2 represents the white player.

    Preconditions:
        - board_size >= 2
        - board_size % 2 == 0
    """
    results = []
    game = reversi.ReversiGame()
    game.set_board_size(board_size)
    for _ in range(iterations):
        game = reversi.ReversiGame()
        prev_move = (-1, -1)
        while game.get_winner() is None:
            move = player1.make_move(game, prev_move)
            game.try_make_move(move)
            if game.get_winner() is None:
                prev_move = player2.make_move(game, move)
                game.try_make_move(prev_move)
        results.append(game.get_winner())
    stats.plot_game_statistics(game, results, 'black', player1, player2)


if __name__ == '__main__':
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()
    #
    # import doctest
    # doctest.testmod()
    #
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['ai_players',
    #                       'reversi',
    #                       'stats'],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['E1136']
    # })

    generate_stats(ai_players.MinimaxABPlayer(2, 16), ai_players.RandomPlayer(), 16, 200)
