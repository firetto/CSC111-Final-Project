"""
statistics.py:
Plots the relevant statistics graphs for the players.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""
from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ai_players
import reversi


def plot_game_statistics(game: reversi.ReversiGame, results: list[str], focused_player: str,
                         focused_type: ai_players.Player, other_type: ai_players.Player) -> None:
    """ Plots two graphs: the first graph shows the results of the games, with a win by the
    focused_player represented by 1, a win by the other player represented by 0, and a draw
    represented by 0.5. The second graph shows the cumulative win probability of the focused_player
    as well as their win probability for the most recent 50 games.

    focused_type is the type of player used for the focused_player. other_type is the type of player
    that was used as the opponent of focused_player.

    game is needed to see whether this was a human vs AI game, and to show this on the graph.

    Draws are counted as 'half-wins' for the player: when calculating the win probability of a
    certain player, a value of 0.5 is added to total sum of the wins for that player.

    Note: a lot of this code draws from Assignment 2.

    Preconditions:
        - all(result in {'white', 'black', 'draw'} for result in results)
        - focused_player in {'white', 'black'}
    """
    if focused_player == 'white':
        other_player = 'black'
    else:
        other_player = 'white'

    outcomes = []
    for result in results:
        if result == focused_player:
            outcomes.append(1)
        elif result == 'draw':
            outcomes.append(0.5)
        else:
            outcomes.append(0)

    cumulative_win_probability = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
    rolling_win_probability = \
        [sum(outcomes[max(i - 50, 0):i]) / min(50, i) for i in range(1, len(outcomes) + 1)]

    fig = make_subplots(rows=2, cols=1)

    if focused_player == 'white':
        fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                                 name='Outcome (1 = White win, 0.5 = Draw, 0 = Black win)'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(y=cumulative_win_probability, mode='lines',
                                 name='White win percentage (cumulative)'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(y=rolling_win_probability, mode='lines',
                                 name='White win percentage (most recent 50 games)'),
                      row=2, col=1)

    else:
        fig.add_trace(go.Scatter(y=outcomes, mode='markers',
                                 name='Outcome (1 = Black win, 0.5 = Draw, 0 = White win)'),
                      row=1, col=1)
        fig.add_trace(go.Scatter(y=cumulative_win_probability, mode='lines',
                                 name='Black win percentage (cumulative)'),
                      row=2, col=1)
        fig.add_trace(go.Scatter(y=rolling_win_probability, mode='lines',
                                 name='Black win percentage (most recent 50 games)'),
                      row=2, col=1)

    fig.update_yaxes(range=[0.0, 1.0], row=2, col=1)

    focused_str = player_to_string(game, focused_player, focused_type)
    other_str = player_to_string(game, other_player, other_type)

    if focused_player == 'white':
        fig.update_layout(
            title='Reversi Game Results | White: ' + focused_str + ', Black: ' + other_str,
            xaxis_title='Game')
    else:
        fig.update_layout(
            title='Reversi Game Results | White: ' + other_str + ', Black: ' + focused_str,
            xaxis_title='Game')

    fig.show()
    fig.write_image('stats.png')


def player_to_string(game: reversi.ReversiGame, player_colour: str, player: ai_players.Player) \
        -> str:
    """ Returns the string representation of the type of the player.

    Preconditions:
        - player_colour in {'white', 'black'}
    """
    if game.get_human_player() == 1 and player_colour == 'black':
        return 'Human'
    elif game.get_human_player() == -1 and player_colour == 'white':
        return 'Human'
    else:
        # the player is one of the AI players
        if isinstance(player, ai_players.RandomPlayer):
            return 'Random Moves'
        elif (isinstance(player, ai_players.MinimaxPlayer)
              or isinstance(player, ai_players.MinimaxABPlayer)):
            return 'Minimax ' + str(player.depth)


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['plotly.graph_objects',
                          'plotly.subplots',
                          'ai_players',
                          'reversi'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
