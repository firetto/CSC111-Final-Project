"""
ui_handler.py
Contains methods for adding UI elements to the window.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import window
import pygame
from reversi import ReversiGame
from typing import List, Dict
from stats import plot_game_statistics
from ai_players import RandomPlayer, MinimaxPlayer, MinimaxABPlayer, \
    POSITIONAL_HEURISTIC, basic_heuristic

# Parameter for the board size stored by the selection
board_size_current = 8

# Whether or not the game is paused.
game_paused = False

def helper_dropdown_select_player(g: ReversiGame, text: str) -> None:
    """HELPER FUNCTION: Select the players given the dropdown option selected."""

    if text == "Human vs. AI":
        g.start_game(human_player=1)
    elif text == "AI vs. Human":
        g.start_game(human_player=-1)
    else:
        g.start_game(human_player=0)

def dropdown_select_player(g: ReversiGame) -> any:
    """Return a function for setting the players given the selected dropdown option."""
    return lambda text: helper_dropdown_select_player(g, text)


def helper_dropdown_select_ai(black: int, colour_to_player: Dict, text: str) -> None:
    """Set the AI given the text.

    Preconditions:
        - text in {'Minimax 2', 'Minimax 3', 'Minimax 4', 'Minimax 8', 'Random Moves'}
    """

    if text.startswith('Minimax '):
        colour_to_player.update({black: MinimaxABPlayer(int(text.split("Minimax ")[-1]),
                                                        board_size_current)})
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


def button_pause_game(w: window.Window) -> None:
    """Function to call when the Pause/Resume game button is pressed.
    Toggle the game_paused attribute, and change the text of the button accordingly."""

    global game_paused

    game_paused = not game_paused

    if game_paused:
        w.get_ui_element('button-pause-game').set_text('Resume Game')
    else:
        w.get_ui_element('button-pause-game').set_text('Pause Game')


def get_game_paused() -> bool:
    """Return game_paused."""

    global game_paused

    return game_paused


def add_ui(w: window.Window, g: ReversiGame, results: List, colour_to_player: Dict) -> None:
    """
    Add some UI to the window, such as buttons, and more.
    """

    w.add_button(rect=pygame.Rect(725, 30, 150, 40),
                 label="button-pause-game", text="Pause Game",
                 function=lambda: button_pause_game(w))

    w.add_text(label="text-choose-players", text="Choose Players", position=(720, 100))
    w.add_dropdown(options_list=["Human vs. AI", "AI vs. Human", 'AI vs. AI'],
                   starting_option="Human vs. AI",
                   rect=pygame.Rect(725, 130, 150, 50),
                   label="dropdown-player",
                   function=dropdown_select_player(g))

    w.add_text(label="text-choose-ai", text="Choose AI types", position=(720, 250))
    w.add_text(label="text-choose-ai-black", text="Black AI", position=(705, 280),
               large_font=False)
    w.add_text(label="text-choose-ai-white", text="White AI", position=(840, 280),
               large_font=False)

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3',
                                 'Minimax 4', 'Minimax 6'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(675, 300, 125, 40),
                   label="dropdown-ai-black",
                   function=dropdown_select_ai(1, colour_to_player))

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3',
                                 'Minimax 4', 'Minimax 6'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(810, 300, 125, 40),
                   label="dropdown-ai-white",
                   function=dropdown_select_ai(-1, colour_to_player))

    w.add_text(label="text-choose-board-size", text="Choose Board Size", position=(700, 450))
    w.add_dropdown(options_list=["8x8", '12x12', '16x16', '24x24'],
                   starting_option="8x8",
                   rect=pygame.Rect(725, 480, 150, 40),
                   label="dropdown-board-size",
                   function=dropdown_select_board_size(g, colour_to_player))

    w.add_button(rect=pygame.Rect(675, 610, 125, 40),
                 label="button-show-stats", text="View Stats",
                 function=lambda: plot_game_statistics(g, results, 'black', colour_to_player[1],
                                                       colour_to_player[-1]))

    w.add_button(rect=pygame.Rect(810, 610, 125, 40),
                 label="button-clear-stats", text="Clear Stats",
                 function=lambda: clear_results(results, w))

    w.add_text(label="text-games-stored", text="Games Stored: 0", position=(720, 665))
