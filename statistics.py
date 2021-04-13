"""
statistics.py:
Plots the relevant statistics graphs for the players.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""
from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_game_statistics(results: list[str], focused_player: str):
    """ Plots two graphs: the first graph shows the results of the games, with a win by the
    focused_player represented by 1, a win by the other player represented by 0, and a draw
    represented by 0.5. The second graph shows the cumulative win probability of the focused_player
    as well as their win probability for the most recent 50 games.

    Note: fig.show() is commented out, since it doesn't work on my computer

    Preconditions:
        - focused_player in {'White', 'Black'}
    """
    outcomes = []
    for result in results:
        if result == focused_player:
            outcomes.append(1)
        elif result == 'Draw':
            outcomes.append(0.5)
        else:
            outcomes.append(0)

    cumulative_win_probability = [sum(outcomes[0:i]) / i for i in range(1, len(outcomes) + 1)]
    rolling_win_probability = \
        [sum(outcomes[max(i - 50, 0):i]) / min(50, i) for i in range(1, len(outcomes) + 1)]

    fig = make_subplots(rows=2, cols=1)

    if focused_player == 'White':
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

    fig.update_layout(title='Reversi Game Results', xaxis_title='Game')
    # fig.show()
    fig.write_image('stats.png')


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
