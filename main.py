"""
main.py
Launch the program from here!
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from ui_handler import add_ui, update_games_stored_text
from window import Window
import reversi
from reversi import ReversiGame
from board import Board
from board_manager import BoardManager
from ai_players import RandomPlayer, MinimaxPlayer
from statistics import plot_game_statistics

if __name__ == "__main__":

    # Initialize PyGame
    pygame.init()

    # Create a window wrapper class instance
    window = Window()

    # Create a ReversiGame instance
    # Change human_player to 1 or -1 to play against AI, 0 if no human player
    game = ReversiGame(human_player=1)  # Set to 1 by default.

    # Setup the BoardManager instance
    board_manager = BoardManager(window)

    # Minimax Player

    # player1 = MinimaxPlayer(2)
    # player2 = RandomPlayer()
    colour_to_player = {1: MinimaxPlayer(2), -1: MinimaxPlayer(2)}

    # List of moves made
    moves_made = [(-1, -1)]

    # List of game win results
    results = []

    # Add UI to the window
    add_ui(window, game, results, colour_to_player)

    # Window loop
    while window.is_running():

        """ UPDATE STUFF """

        # Get game winner
        winner = game.get_winner()
        if winner is not None:
            results.append(winner)
            update_games_stored_text(len(results), window)
            print(winner)
            game.start_game(human_player=game.get_human_player())

        if game.get_human_player() == game.get_current_player():          
            # Look at the mouse clicks and see if they are in the board.
            
            for event in window.get_events():
                if event[0] == pygame.MOUSEBUTTONUP:
                    square = board_manager.check_mouse_press(event[1], game.get_board())
                    if square != (-1, -1):
                        if game.try_make_move(square):
                            moves_made.append(square)
        elif game.get_winner() is None:
            moves_made.append(game.try_make_move(colour_to_player[game.get_current_player()]
                                                 .make_move(game, moves_made[-1])))

        # Update the window's clock
        window.update_clock()

        """ DRAW STUFF """

        # Draw the background first!!!!
        window.draw_background()

        # Draw the board.
        board_manager.draw_board(game.get_board())

        # Draw the buttons etc.
        window.draw_ui()

        # Draw the rest of the stuff and update the window!
        window.update()

    # Once loop ends, quit pygame.
    pygame.quit()
