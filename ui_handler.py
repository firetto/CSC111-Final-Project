"""
ui_handler.py
Contains methods for adding UI elements to the window.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import window
import pygame
from reversi import ReversiGame
from typing import List, Dict
from statistics import plot_game_statistics
from ai_players import RandomPlayer, MinimaxPlayer, MinimaxABPlayer, \
    POSITIONAL_HEURISTIC, basic_heuristic

# Parameter for the board size stored by the selection
board_size_current = 8





def dropdown_select_player(g: ReversiGame) -> any:
    """Holy crap."""
    return lambda text: g.start_game(human_player=1) if text == 'Human vs. AI' else (
        g.start_game(human_player=-1) if text == 'AI vs. Human' else g.start_game(human_player=0))

def helper_dropdown_select_ai(black: int, colour_to_player: Dict, text: str) -> None:
    """Set the AI given the text.

    Preconditions:
        - text in {'Minimax 2', 'Minimax 3', 'Minimax 4', 'Minimax 8', 'Random Moves'}
    """

    if text == 'Minimax 2':
        colour_to_player.update({black: MinimaxABPlayer(2, board_size_current)})
    elif text == 'Minimax 3':
        colour_to_player.update({black: MinimaxABPlayer(3, board_size_current)})
    elif text == 'Minimax 4':
        colour_to_player.update({black: MinimaxABPlayer(4, board_size_current)})
    elif text == 'Minimax 6':
        colour_to_player.update({black: MinimaxABPlayer(6, board_size_current)})
    else:
        colour_to_player.update({black: RandomPlayer()})


def dropdown_select_ai(black: int, colour_to_player: Dict) -> any:
    """Return a function for setting the AI given the text."""

    return lambda text: helper_dropdown_select_ai(black, colour_to_player, text)


def helper_dropdown_select_board_size(g: ReversiGame, colour_to_player: Dict, text: str) -> None:
    """
    Set the board size given the text.
    Preconditions:
        - text is of the form '<int>x<int>' where the two integers are the same and greater than 0.
    """
    global board_size_current

    # Update the current board size (why?)
    board_size_current = int(text.split('x')[0])

    # Set new heuristics for players
    colour_to_player[1].set_heuristic(board_size_current)

    colour_to_player[-1].set_heuristic(board_size_current)

    # Update game board size
    g.set_board_size(board_size_current)

    # Start new game.
    g.start_game(human_player=g.get_human_player())


def dropdown_select_board_size(g: ReversiGame, colour_to_player: Dict) -> any:
    """Return a function for setting the board size given the text.
    Preconditions:
     - text is of the form '<int>x<int>' where the two integers are the same.
    """

    return lambda text: helper_dropdown_select_board_size(g, colour_to_player, text)


def update_games_stored_text(games: int, w: window.Window) -> None:
    """Update the 'Games Stored' label with to display 'Games Stored: <games>'."""
    w.get_ui_element('text-games-stored').set_text(f'Games Stored: {games}')


def clear_results(results: List, w: window.Window) -> None:
    """Clear the results list by MUTATING it and update the Games Store text accordingly."""

    results.clear()

    update_games_stored_text(0, w)


def add_ui(w: window.Window, g: ReversiGame, results: List, colour_to_player: Dict) -> None:
    """
    Add some UI to the window, such as buttons, and more.
    """

    w.add_dropdown(options_list=["Human vs. AI", "AI vs. Human", 'AI vs. AI'],
                   starting_option="Human vs. AI",
                   rect=pygame.Rect(725, 60, 150, 50),
                   label="dropdown-player",
                   function=dropdown_select_player(g))

    w.add_text(label="text-choose-players", text="Choose Players", position=(720, 30))

    w.add_text(label="text-choose-ai", text="Choose AI types", position=(720, 180))
    w.add_text(label="text-choose-ai-black", text="Black AI", position=(705, 210),
               large_font=False)
    w.add_text(label="text-choose-ai-white", text="White AI", position=(840, 210),
               large_font=False)

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3',
                                 'Minimax 4', 'Minimax 6'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(675, 230, 125, 50),
                   label="dropdown-ai-black",
                   function=dropdown_select_ai(1, colour_to_player))

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3',
                                 'Minimax 4', 'Minimax 6'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(810, 230, 125, 50),
                   label="dropdown-ai-white",
                   function=dropdown_select_ai(-1, colour_to_player))

    w.add_text(label="text-choose-board-size", text="Choose Board Size", position=(700, 390))
    w.add_dropdown(options_list=["8x8", '12x12', '16x16', '24x24'],
                   starting_option="8x8",
                   rect=pygame.Rect(725, 420, 150, 50),
                   label="dropdown-board-size",
                   function=dropdown_select_board_size(g, colour_to_player))

    w.add_button(rect=pygame.Rect(725, 560, 150, 40),
                 label="button-show-stats", text="View Statistics",
                 function=lambda: plot_game_statistics(g, results, 'black', colour_to_player[1],
                                                       colour_to_player[-1]))

    w.add_button(rect=pygame.Rect(725, 610, 150, 40),
                 label="button-clear-stats", text="Clear Statistics",
                 function=lambda: clear_results(results, w))

    w.add_text(label="text-games-stored", text="Games Stored: 0", position=(720, 665))
