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
from ai_players import RandomPlayer, MinimaxPlayer, POSITIONAL_HEURISTIC, basic_heuristic


def dropdown_select_player(g: ReversiGame) -> any:
    """Holy crap."""
    return lambda text: g.start_game(human_player=1) if text == 'Human vs. AI' else (
        g.start_game(human_player=-1) if text == 'AI vs. Human' else g.start_game(human_player=0))


def dropdown_select_ai(black: int, colour_to_player: Dict) -> any:
    """Return a function for setting the AI given the text."""

    if black:
        return lambda text: colour_to_player.update({black:
                                                     MinimaxPlayer(2, basic_heuristic(8)) if text == 'Minimax 2'
                                                     else (
                                                           MinimaxPlayer(3, POSITIONAL_HEURISTIC) if text == 'Minimax 3'
                                                           else RandomPlayer())})


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

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(675, 230, 125, 50),
                   label="dropdown-ai-black",
                   function=dropdown_select_ai(1, colour_to_player))

    w.add_dropdown(options_list=["Random Moves", "Minimax 2", 'Minimax 3'],
                   starting_option="Minimax 2",
                   rect=pygame.Rect(810, 230, 125, 50),
                   label="dropdown-ai-white",
                   function=dropdown_select_ai(-1, colour_to_player))

    w.add_button(rect=pygame.Rect(725, 530, 150, 50),
                 label="button-show-stats", text="View Statistics",
                 function=lambda: plot_game_statistics(g, results, 'Black', colour_to_player[1],
                                                       colour_to_player[-1]))

    w.add_button(rect=pygame.Rect(725, 590, 150, 50),
                 label="button-clear-stats", text="Clear Statistics",
                 function=lambda: clear_results(results, w))

    w.add_text(label="text-games-stored", text="Games Stored: 0", position=(720, 665))
